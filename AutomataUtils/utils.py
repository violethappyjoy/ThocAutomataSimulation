import tkinter as tk
from tkinter import filedialog
import networkx as nx
import matplotlib.pyplot as plt


status_label = None  # Define status_label globally
nfa_filename_entry = None  # Define nfa_filename_entry globally

def delta(state, alphabet, rules, dfa):
    """
    Find result of state for every input
    """
    result = []
    for letter in alphabet:
        res = ''
        for a in state:
            for idx in rules:
                if idx[0] == str(a) and idx[1] == letter:
                    if idx[2] not in res:
                        res += idx[2]
        result.append(''.join(sorted(res)))
    dfa[state] = result


def set_final_states(final, dfa_dict):
    """
    Set final states of DFA
    """
    new_final_state = []
    for init_final_state in final:
        for state in dfa_dict.keys():
            if init_final_state in state:
                new_final_state.append(state)
    return new_final_state


def states_queue(dfa_dict):
    """
    Accessible states that have yet to be checked
    """
    temp = []
    for state in dfa_dict:
        for x in dfa_dict[state]:
            if (x not in dfa_dict.keys()) and x:
                temp.append(x)
    return temp


def export_file(dfa_dict, alphabet, initial, final):
    """
    Create and export to file
    """
    dfa_output = open("DFA.txt", "w")
    dfa_output.write(f"{len(dfa_dict)}\t\t//Number of states\n")

    for a in alphabet:
        dfa_output.write(a)
    dfa_output.write(f"\t\t// {len(alphabet)} symbols in the alphabet\n")

    dfa_output.write(f"{initial}\t\t// Initial state(s)\n")

    for f in final:
        dfa_output.write(f"{f} ")
    dfa_output.write(f"\t\t// Final state(s)\n")

    for state in dfa_dict:
        i = 0
        for result in dfa_dict[state]:
            if state == '':
                state = '_'
            if result == '':
                result = '_'
            dfa_output.write(f"{state} {alphabet[i]} {result}\n")
            i += 1
    dfa_output.close()

    print("DFA.txt file created successfully.")  # Add this line

    # Visualization
    G = nx.DiGraph()

    for state, transitions in dfa_dict.items():
        for symbol, next_state in zip(alphabet, transitions):
            G.add_edge(state, next_state, label=symbol)

    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, arrows=True)
    nx.draw_networkx_nodes(G, pos, nodelist=[initial], node_color='g', node_size=500)
    nx.draw_networkx_nodes(G, pos, nodelist=final, node_color='r', node_size=500)
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title('DFA')
    plt.show()



def main():
    dfa_result_dict = {}
    states_to_examine = []
    alphabet = []
    rules = []

    # Open and read from file
    nfa_input = open("NFA.txt", "r").readlines()

    count = 0
    states_num = 0
    initial_state = ''
    final_states = ''

    for line in nfa_input:
        line = line.split("//")
        if count == 0:
            states_num = int(line[0])
        elif count == 1:
            alphabet = list(line[0].strip())
        elif count == 2:
            initial_state = str(line[0]).strip()
        elif count == 3:
            final_states = (str(line[0]).strip())
        else:
            rules.append(line[0].strip())
        count += 1

    final_states = list(final_states)

    # Check if states (n) & inputs (m) < 10
    if len(alphabet) > 10:
        print("Error: Too many inputs.")
    if states_num > 10:
        print("Error: Too many states.")

    states_to_examine.append(initial_state)

    while True:
        for state in states_to_examine:
            delta(state, alphabet, rules, dfa_result_dict)
            states_to_examine = states_queue(dfa_result_dict).copy()

        if not states_to_examine:
            break

    final_states = (set_final_states(final_states, dfa_result_dict)).copy()

    export_file(dfa_result_dict, alphabet, initial_state, final_states)
    print(f"\n{dfa_result_dict}")


import networkx as nx
import matplotlib.pyplot as plt


def visualize_nfa_from_file(nfa_filename):
    try:
        print("Visualizing NFA...")

        # Open and read from file
        with open(nfa_filename, "r") as file:
            lines = file.readlines()

        # Extract NFA information from the file
        states_num = int(lines[0].strip())
        alphabet = list(lines[1].strip())
        initial_state = lines[2].strip()
        final_states = lines[3].strip().split()
        transitions = [line.strip().split() for line in lines[4:]]

        print("States:", states_num)
        print("Alphabet:", alphabet)
        print("Initial state:", initial_state)
        print("Final states:", final_states)
        print("Transitions:", transitions)

        # Create the NFA graph
        G = nx.MultiDiGraph()

        # Add transitions
        for transition in transitions:
            start_state, symbol, end_state = transition
            label = f"{symbol}"
            if start_state == end_state:  # Check for self-loop
                label ="        "+f"{symbol}"
            G.add_edge(int(start_state), int(end_state), label=label)

        # Mark initial and final states
        G.nodes[int(initial_state)]['color'] = 'green'
        for state in final_states:
            G.nodes[int(state)]['color'] = 'red'

        # Visualization
        pos = nx.spring_layout(G)
        edge_labels = {(n1, n2): d['label'] for n1, n2, d in G.edges(data=True)}
        node_colors = [G.nodes[n].get('color', 'lightblue') for n in G.nodes]

        # Draw NFA
        nx.draw(G, pos, with_labels=True, node_color=node_colors)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
        plt.title('NFA Visualization')
        plt.show()

        print("NFA visualization successful.")
    except Exception as e:
        print(f"Error during visualization: {str(e)}")


# Test the function with a sample NFA file
nfa_filename = "NFA.txt"  # Replace this with the path to your NFA file
visualize_nfa_from_file(nfa_filename)



