import seaborn as sns

from matplotlib import font_manager, rcParams

def set_visualization_style():
    """
    Configure global visualization settings for matplotlib and seaborn.
    This ensures that all plots have a professional and aesthetically pleasing style.
    """
    # Check if Times New Roman is available
    times_new_roman = [
        f for f in font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
        if 'Times New Roman' in f
    ]

    if not times_new_roman:
        print("Warning: Times New Roman is not installed or not found by Matplotlib.")
    else:
        # Manually set the font path to Times New Roman
        font_path = times_new_roman[0]
        times_new_roman_font = font_manager.FontProperties(fname=font_path)
        
        # Apply the font globally
        rcParams['font.family'] = times_new_roman_font.get_name()
        print(f"Using font: {times_new_roman_font.get_name()}")
    
    rcParams['mathtext.fontset'] = 'stix'   # Use Times for math symbols as well
    rcParams['font.size'] = 12          # Set default font size
    rcParams['axes.titlesize'] = 14     # Set font size for plot titles
    rcParams['axes.labelsize'] = 12     # Set font size for axis labels
    rcParams['legend.fontsize'] = 10    # Set font size for legends
    rcParams['xtick.labelsize'] = 10    # Set font size for x-axis ticks
    rcParams['ytick.labelsize'] = 10    # Set font size for y-axis ticks

    # Use high-quality vector output for publication-ready figures
    rcParams['savefig.dpi'] = 400       # Set figure resolution for saving
    rcParams['figure.dpi'] = 400        # Set resolution for inline displays
    rcParams['savefig.format'] = 'pdf'  # Save figures as PDF by default (vector graphics)

    # Customize figure layout and spacing
    rcParams['figure.autolayout'] = True    # Auto-adjust layout to prevent overlaps
    rcParams['axes.spines.top'] = False     # Turn off top spine
    rcParams['axes.spines.right'] = False   # Turn off right spine

    # Improve grid aesthetics
    rcParams['grid.color'] = 'gray'
    rcParams['grid.alpha'] = 0.4
    rcParams['grid.linestyle'] = '--'

    # Adjust line styles for better visibility
    rcParams['lines.linewidth'] = 2     # Thicker lines
    rcParams['lines.markersize'] = 6    # Larger markers for scatter plots

    # Set default colormap for consistency
    rcParams['image.cmap'] = 'viridis'  # Default colormap for heatmaps

    # Configure seaborn for better style
    sns.set_theme(
        style="whitegrid",      # Use a white grid as the base style
        context="notebook",     # Suitable for most applications
        palette="deep"          # Use the deep color palette
    )