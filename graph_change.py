import numpy as np
import matplotlib.pyplot as plt

def plot_disc_graph_change(values, ax):
    # Data points and labels
    labels = ['D', 'I', 'S', 'C']
    
    values24 = [value + 24 for value in values]

    # Define mappings for each label
    mappings = {
        'D': [0, 1, 2, 3, 4, 4, 5, 5, 6, 8, 10, 11, 12, 18, 23, 24, 25, 27, 30, 32, 34, 36, 37, 38, 38, 43, 44, 45, 46, 47, 50, 53, 56, 59, 64, 65, 66, 68, 70, 72, 73, 73, 74, 75, 76, 77, 78, 78, 79, 80 ],
        'I': [0, 1, 1, 2, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 9, 12, 16, 18, 23, 25, 30, 32, 38, 41, 43, 45, 47, 55, 59, 62, 66, 68, 72, 73, 75, 75, 75, 75, 76, 76, 76, 76, 77, 77, 77, 78, 78, 79, 79, 80],
        'S': [0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 5, 6, 7, 8, 9, 16, 18, 23, 25, 30, 32, 34, 36, 38, 45, 48, 50, 55, 57, 59, 62, 64, 66, 68, 70, 72, 73, 74, 75, 75, 76, 76, 76, 77, 77, 77, 77, 78, 79, 80],
        'C': [0, 1, 1, 2, 3, 4, 4, 5, 5, 6, 7, 9, 10, 11, 12, 16, 18, 23, 25, 27, 36, 38, 43, 45, 48, 55, 59, 62, 68, 69, 70, 71, 72, 72, 73, 74, 75, 75, 76, 76, 77, 77, 78, 78, 78, 79, 79, 79, 80, 80]
    }


    # Transform original values using mappings
    mapped_values = [mappings[label][value] for label, value in zip(labels, values24)]

    # Plot the line graph
    positions = np.arange(len(labels))  # x positions for the labels
    ax.plot(positions, mapped_values, marker='o', linestyle='-', markersize=5, color='#278D8D')  # Connect points with a line


    ax.set_title("Graph 3 | CHANGE\n", fontsize=20, fontweight='bold')
    ax.set_title("Mirror, Perceived Self", fontsize=15, fontweight='bold', loc='right', color='gray')

    # Custom grid lines as specified in previous configuration
    line_styles = {10: ('dotted', 0.5), 20: ('dotted', 1.5), 30: ('dotted', 0.5),
                40: ('solid', 1.5), 50: ('dotted', 0.5), 60: ('dotted', 1.5), 70: ('dotted', 0.5)}
    for y, (style, width) in line_styles.items():
        ax.axhline(y=y, linestyle=style, linewidth=width, color='gray')

    # Set y-axis to range from 0 to 80
    ax.set_ylim(0, 80)
    ax.set_yticks(np.arange(0, 81, 10))

    # Hide y-axis tick labels
    for label in ax.get_yticklabels():
        label.set_visible(False)


    # Update x-axis settings
    ax.set_xticks(positions)
    ax.set_xticklabels(['']*len(labels))  # Set empty labels for x-axis

    ax.spines['bottom'].set_visible(False)  # Hide the bottom spine
    ax.spines['left'].set_visible(False)  # Optionally, hide the left spine if preferred

    # Create a secondary x-axis at the top
    ax2 = ax.twiny()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_xticks(positions)
    ax2.set_xticklabels(labels)
    ax2.spines['top'].set_visible(False)  # Optionally hide the top spine if preferred
    
        
    for i, value in enumerate(values):
        ax.text(positions[i], mapped_values[i] + 1, f'{value}', ha='right', fontsize=12, color='#278D8D')


    return ax 