from PIL import Image, ImageDraw
import tkinter as tk
from PIL import ImageTk

x_offset = 800
y_offset = 3100

class MapImageHandler:
    def __init__(self, map_image_path, station_order_dictionary):
        self.station_coordinates = {
            "Parliament": (3618 + x_offset, 1264 + y_offset, 4134 + x_offset, 1393 + y_offset),
            "Jolimont": (4277 + x_offset, 1715 + y_offset, 4700 + x_offset, 1837 + y_offset),
            "Richmond": (4327 + x_offset, 2732 + y_offset, 4807 + x_offset, 2832 + y_offset),
            "Flinders Street": (2616 + x_offset, 2732 + y_offset, 3325 + x_offset, 2832 + y_offset),
            "Southern Cross": (431 + x_offset, 1264 + y_offset, 1162 + x_offset, 1378 + y_offset),
            "Melbourne Central": (2716 + x_offset, 376 + y_offset, 3217 + x_offset, 619 + y_offset),
            "Flagstaff": (2351 + x_offset, 168 + y_offset, 2494 + x_offset, 619 + y_offset),
            "North Melbourne": (360 + x_offset, 361 + y_offset, 1155 + x_offset, 490 + y_offset),
            "South Kensington": (-213 + x_offset, 383 + y_offset, 331 + x_offset, 641 + y_offset),
            "Footscray": (-765 + x_offset, -269 + y_offset, -299 + x_offset, -133 + y_offset),
            "Macaulay": (3074 + x_offset, -548 + y_offset, 3518 + x_offset, -412 + y_offset),
            "Flemington Bridge": (3079 + x_offset, -731 + y_offset, 3910 + x_offset, -621 + y_offset),
            "Royal Park": (3071 + x_offset, -935 + y_offset, 3582 + x_offset, -811 + y_offset),
            "Jewell": (3064 + x_offset, -1146 + y_offset, 3414 + x_offset, -1008 + y_offset),
            "Brunswick": (3071 + x_offset, -1329 + y_offset, 3567 + x_offset, -1234 + y_offset),
            "Anstey": (3086 + x_offset, -1540 + y_offset, 3421 + x_offset, -1423 + y_offset),
            "Moreland": (3071 + x_offset, -1737 + y_offset, 3516 + x_offset, -1613 + y_offset),
            "Coburg": (3071 + x_offset, -1956 + y_offset, 3436 + x_offset, -1817 + y_offset),
            "Batman": (3086 + x_offset, -2123 + y_offset, 3429 + x_offset, -2029 + y_offset),
            "Merlynston": (3057 + x_offset, -2335 + y_offset, 3596 + x_offset, -2211 + y_offset),
            "Fawkner": (3064 + x_offset, -2532 + y_offset, 3487 + x_offset, -2422 + y_offset),
            "Gowrie": (3071 + x_offset, -2736 + y_offset, 3436 + x_offset, -2612 + y_offset),
            "Upfield": (2780 + x_offset, -3071 + y_offset, 3144 + x_offset, -2933 + y_offset),
            "Kensington": (2078 + x_offset, -634 + y_offset, 2616 + x_offset, -527 + y_offset),
            "Newmarket": (2086 + x_offset, -820 + y_offset, 2616 + x_offset, -727 + y_offset),
            "Showgrounds": (990 + x_offset, -1114 + y_offset, 1649 + x_offset, -992 + y_offset),
            "Flemington Racecourse": (295 + x_offset, -992 + y_offset, 861 + x_offset, -749 + y_offset),
            "Ascot Vale": (2071 + x_offset, -1042 + y_offset, 2608 + x_offset, -913 + y_offset),
            "Moonee Ponds": (2071 + x_offset, -1236 + y_offset, 2759 + x_offset, -1099 + y_offset),
            "Essendon": (2071 + x_offset, -1443 + y_offset, 2544 + x_offset, -1314 + y_offset),
        }
        
        self.line_coordinates = {
            "burnley_group": {
                ("Flagstaff", "Melbourne Central"): (2500 + x_offset, 800 + y_offset, 2899 + x_offset, 850 + y_offset),
            }
        }
        self.station_order = station_order_dictionary
        self.map_image = Image.open(map_image_path)
        print('Initalised the map maker')
        
    def highlight_stations(self, affected_stations):
        """
        Highlights stations on the map by covering their areas with white rectangles
        
        Args:
            affected_stations (list): List of station names to highlight
        
        Returns:
            PIL.Image: Modified map image with highlighted stations
        """
        
        print('starting to cover stations')
        # Create a copy of the original image
        modified_map = self.map_image.copy()
        draw = ImageDraw.Draw(modified_map)
        
        # Draw white rectangles for each affected station
        for station in affected_stations:
            if station in self.station_coordinates:
                coords = self.station_coordinates[station]
                draw.rectangle(coords, fill='white')
                print(f'{station} covered')
                
        print('Done covering stations!')
        return modified_map
    
    def highlight_lines(self, modified_map, station1, station2, line):
        print('Starting to cover lines')
        # Create a copy of the original image
        draw = ImageDraw.Draw(modified_map)
        
        # Check if line exists in line_coordinates
        if line in self.line_coordinates:
            # Check if station pair exists in the line
            station_pair = (station1, station2)
            if station_pair in self.line_coordinates[line]:
                coords = self.line_coordinates[line][station_pair]
                draw.rectangle(coords, fill='white')
                print(f'Covered from {station1} to {station2} on the {line}')
            # Check reverse pair
            station_pair = (station2, station1)
            if station_pair in self.line_coordinates[line]:
                coords = self.line_coordinates[line][station_pair]
                draw.rectangle(coords, fill='white')
                print(f'Covered from {station2} to {station2} on the {line}')
        
        print('Done covering lines!')
        return modified_map
    
    def coverStations(self, affected_stations, output_path):
        """
        Saves the modified map with highlighted stations
        
        Args:
            affected_stations (list): List of station names to highlight
            output_path (str): Path where the modified image will be saved
        """
        modified_map = self.highlight_stations(affected_stations)
        
        modified_map.save(output_path)
    
    def coverLines(self, stationPairs, output_path):
        """
        Saves the modified map with highlighted lines between station pairs
        
        Args:
            stationPairs (list): List of tuples containing station pairs and line name (station1, station2, line)
            output_path (str): Path where the modified image will be saved
        """
        modified_map = self.map_image.copy()
        
        # Iterate through each tuple of (station1, station2, line)
        for station1, station2, line in stationPairs:
            modified_map = self.highlight_lines(modified_map, station1, station2, line)
            
        modified_map.save(output_path)
        
        

        


class CoordinateFinder:
    def __init__(self, image_path):
        self.root = tk.Tk()
        self.original_image = Image.open(image_path)
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate scaling factor
        width_ratio = screen_width / self.original_image.width
        height_ratio = screen_height / self.original_image.height
        self.scale = min(width_ratio * 0.8, height_ratio * 0.8)  # 80% of screen size
        
        # Resize image
        new_width = int(self.original_image.width * self.scale)
        new_height = int(self.original_image.height * self.scale)
        self.image = self.original_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.image)
        
        self.canvas = tk.Canvas(self.root, width=new_width, height=new_height)
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.photo, anchor="nw")
        
        self.start_x = None
        self.start_y = None
        self.rect = None
        
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        
    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y
        
    def on_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y, outline="red"
        )
        
    def on_release(self, event):
        # Convert coordinates back to original scale
        original_x1 = int(self.start_x / self.scale)
        original_y1 = int(self.start_y / self.scale)
        original_x2 = int(event.x / self.scale)
        original_y2 = int(event.y / self.scale)
        print(f"Coordinates: ({original_x1 - x_offset}, {original_y1 - y_offset}, {original_x2 - x_offset}, {original_y2 - y_offset})")
        print(f"Copyable: ({original_x1 - x_offset} + x_offset, {original_y1 - y_offset} + y_offset, {original_x2 - x_offset} + x_offset, {original_y2 - y_offset} + y_offset),")
        
    def run(self):
        self.root.mainloop()

# Run coord finder
# if __name__ == "__main__":
# finder = CoordinateFinder("utils/trainlogger/map/base.png")
# finder.run()