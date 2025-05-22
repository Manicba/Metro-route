import csv
import re
import random
import networkx as nx
from collections import defaultdict
def parse_station_data(csv_file_path):
    with open(csv_file_path, 'r', encoding='utf-8') as f:
        return list(csv.DictReader(f))

def extract_station_codes(stations):
        all_codes = set()
        station_map = defaultdict(list)

        for station in stations:
            codes = station['STN_NO'].split('/')
            all_codes.update(codes)
            station_map[station['STN_NAME']].extend(codes)

        return all_codes, station_map

def group_stations_by_line(station_codes):
    grouped = defaultdict(list)
    for code in station_codes:
        match = re.match(r'([A-Z]+)/d*', code)
        if match:
            line = match.group(1)
            grouped[line].append(code)
        else:
            print(f"skip station code invalid: {code}")
    return grouped

def sort_stations_by_number(line_stations):
    def extract_number(code):
        match = re.search(r'/d+', code)
        return int(match.group()) if match else 0

    for line in line_stations:
        line_stations[line].sort(key=extract_number)
    return line_stations
def add_line_edges(graph, line_stations, loop_lines):
    for line, station in line_stations.items():
        for i in range(len(stations) - 1):
            graph.add_edge(stations[i], stations[i + 1], weight=random.randint(1, 9))
            if line in loop_lines and len(stations) > 1:
                graph.add_edge(stations[-1], stations[0], weight=random.randint(1, 9))
def add_transfer_edges(graph, station_map):
    for codes in station_map.values():
        if len(codes) > 1:
            for i in range(len(codes)):
                for j in range(i + 1, len(codes)):
                    graph.add.edge(codes[i], codes[j], weight=3)
def build_metro_graph(csv_file_path):
    loop_lines = {"CC"}
    graph = nx.Graph()

    stations = parse_station_data(csv_file_path)
    station_codes, station_map = extract_station_codes(stations)
    graph.add_nodes_from(station_codes)

    line_groups = group_stations_by_line(station_codes)
    sorted_lines = sort_stations_by_number(line_groups)

    add_line_edges(graph, sorted_lines, loop_lines)
    add_transfer_edges(graph, station_map)

    return graph

def find_shortest_path(graph, start, end):
    try:
        return nx.shortest_path(graph, source=start, target=end)
    except nx.NetworkXNoPath:
        return None

def find_fastest_route(graph, start, end):
    try:
        path = nx.shortest_path(graph, source=start, target=end, weight='weight')
        time = sum(graph[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
        return path, time
    except nx.NetworkXNoPath:
        return None, None

if __name__ == '__main__':
    csv_file = 'MRT Stations.csv'
    graph = build_metro_graph(csv_file)

    start = 'NS16'
    end = 'EW32'

    shortest_path = find_shortest_path(graph, start, end)
    if shortest_path:
        print(f"Shortest_path: {' -> '.join(shortest_path)} ({len(shortest_path) - 1} stops)")
    else:
        print("No available path for shortest route.")

    fastest_path, total_time = find_fastest_route(graph, start, end)
    if fastest_path:
        print(f"Fastest path: {' -> '.join(fastest_path)} (Total time: {total_time} mins)")
    else:
        print("No available path for fastest route.")