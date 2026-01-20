import os
from PIL import Image, ImageSequence

def coalesce_and_reverse(input_path):
    print(f"Processing: {input_path}...")
    
    with Image.open(input_path) as im:
        if not im.is_animated:
            print(f"Skipping {input_path} (not a GIF)")
            return

        # 1. COALESCE: Rebuild every frame to be a full image
        # (This prevents "glitching" when we mess with the order)
        frames = []
        
        # Create a background canvas (using the first frame's mode)
        # We start with a blank canvas
        canvas = im.copy().convert("RGBA")
        
        for frame in ImageSequence.Iterator(im):
            # Draw the current frame onto the canvas
            # We must use 'convert' to handle transparency/indexing correctly
            frame = frame.convert("RGBA")
            canvas.paste(frame, (0, 0), frame)
            
            # Add this complete frame to our list
            frames.append(canvas.copy())

        # 2. REVERSE: Flip the list of frames
        frames.reverse()

        # 3. SAVE: Overwrite the file (or change name to 'rev_' + input_path)
        # Duration is grabbed from the original GIF info
        original_duration = im.info.get('duration', 100)
        
        frames[0].save(
            input_path, 
            save_all=True, 
            append_images=frames[1:], 
            loop=0, 
            duration=original_duration,
            disposal=2  # Clears the frame before drawing the next (safer for reversed anims)
        )
        print(f"Done! Reversed {input_path}")

# --- Main Loop ---
# Finds all .gif files in the current folder
folder = "." 

for filename in os.listdir(folder):
    if filename.lower().endswith(".gif"):
        try:
            coalesce_and_reverse(filename)
        except Exception as e:
            print(f"Error processing {filename}: {e}")

print("All finished.")