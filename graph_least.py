import numpy as np
import matplotlib.pyplot as plt

def plot_disc_graph_least(values, ax):
    # Data points and labels
    labels = ['D', 'I', 'S', 'C']

    # Define mappings for each label
    mappings = {
        'D': [3, 7, 18, 27, 33, 37, 42, 46, 47, 53, 55, 58, 62, 66, 68, 71, 73, 74, 75, 76, 77, 78, 79, 79, 80],
        'I': [5, 10, 21, 27, 37, 42, 50, 58, 63, 66, 71, 73, 75, 77, 77, 78, 78, 78, 79,79, 79, 80, 80, 80, 80],
        'S': [3, 5, 10, 21, 27, 33, 37, 46, 50, 55, 63, 66, 71, 73, 74, 75, 76, 77, 78, 79, 80, 80, 80, 80, 80],
        'C': [3, 5, 13, 21, 27, 33, 37, 42, 46, 53, 57, 66, 68, 71, 73, 75, 76, 77, 78, 79, 79, 80, 80, 80, 80]
    }

    # Transform original values using mappings
    mapped_values = [mappings[label][value] for label, value in zip(labels, values)]

    # Plot the line graph
    positions = np.arange(len(labels))  # x positions for the labels
    ax.plot(positions, mapped_values, marker='o', linestyle='-', markersize=5, color='#A00100')  # Connect points with a line


    ax.set_title("Graph 2 | LEAST\n", fontsize=20, fontweight='bold')
    ax.set_title("Core, Private Self", fontsize=15, fontweight='bold', loc='right', color='gray')

    # Custom grid lines as specified in previous configuration
    line_styles = {10: ('dotted', 0.5), 20: ('dotted', 1.5), 30: ('dotted', 0.5),
                40: ('solid', 1.5), 50: ('dotted', 0.5), 60: ('dotted', 1.5), 70: ('dotted', 0.5)}
    for y, (style, width) in line_styles.items():
        ax.axhline(y=y, linestyle=style, linewidth=width, color='gray')

    # Set y-axis to range from 0 to 80
    ax.set_ylim(80, 0)  # Set the limits from high to low to invert the axis
    ax.set_yticks(np.arange(0, 81, 10))

    # Hide y-axis tick labels
    for label in ax.get_yticklabels():
        label.set_visible(False)

    # Since the y-axis is inverted, if hiding the labels isn't enough and you want custom labels showing
    # 0 at the top down to 80 at the bottom, you can explicitly set them like this:
    ax.set_yticklabels([str(y) for y in range(0, 81, 10)][::-1])

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
        ax.text(positions[i], mapped_values[i] - 2, f'{value}', ha='center', fontsize=12, color='#A00100')

    return ax 