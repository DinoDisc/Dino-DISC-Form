import numpy as np
import matplotlib.pyplot as plt

def plot_disc_graph_most(values, ax):
    # Data points and labels
    labels = ['D', 'I', 'S', 'C']

    # Define mappings for each label
    mappings = {
        'D': [9, 14, 20, 28, 32, 35, 39, 43, 45, 50, 55, 57, 59, 64, 66, 73, 75, 76, 76, 76, 76, 77, 78, 79, 80],
        'I': [4, 16, 28, 35, 45, 55, 57, 66, 68, 70, 73, 75, 76, 76, 76, 76, 76, 76, 76, 77, 77, 78, 78, 79, 80],
        'S': [12, 18, 22, 32, 37, 43, 45, 53, 55, 59, 64, 66, 68, 70, 73, 73, 74, 74, 75, 76, 77, 78, 79, 80, 80],
        'C': [9, 16, 22, 32, 43, 50, 55, 66, 68, 70, 71, 73, 74, 75, 75, 76, 76, 77, 77, 78, 78, 79, 79, 80, 80]
    }

    # Transform original values using mappings
    mapped_values = [mappings[label][value] for label, value in zip(labels, values)]

    # Plot the line graph
    positions = np.arange(len(labels))  # x positions for the labels
    ax.plot(positions, mapped_values, marker='o', linestyle='-', markersize=5, color='#1C80BC')  # Connect points with a line

    ax.set_title("Graph 1 | MOST\n", fontsize=20, fontweight='bold')
    ax.set_title("Mask, Public Self", fontsize=15, fontweight='bold', loc='right', color='gray')

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

        # Label the points with original values
    for i, value in enumerate(values):
        ax.text(positions[i], mapped_values[i] + 1, f'{value}', ha='center', fontsize=12, color='#1C80BC')

    
    return ax 