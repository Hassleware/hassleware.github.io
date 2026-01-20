import os
from PIL import Image, ImageEnhance

def process_gifs():
    current_dir = os.getcwd()
    files = [f for f in os.listdir(current_dir) if f.lower().endswith('.gif')]

    if not files:
        print("No .gif files found!")
        return

    print(f"Found {len(files)} GIFs. Processing...")

    for filename in files:
        try:
            # Get the base name (e.g., "1" from "1.gif")
            base_name = os.path.splitext(filename)[0]

            # ---------------------------
            # PART 1: PROCESS IMAGE (Always Overwrite)
            # ---------------------------
            with Image.open(filename) as im:
                # Go to last frame
                last_frame_index = im.n_frames - 1
                im.seek(last_frame_index)

                # Convert to RGBA
                rgba_im = im.convert("RGBA")

                # Create White Background
                white_bg = Image.new("RGB", rgba_im.size, (255, 255, 255))
                white_bg.paste(rgba_im, (0, 0), rgba_im)

                # BOOST VIBRANCY
                enhancer = ImageEnhance.Color(white_bg)
                vibrant_im = enhancer.enhance(1.2) 

                # Save JPG
                jpg_filename = base_name + ".jpg"
                vibrant_im.save(jpg_filename, "JPEG", quality=100, subsampling=0)
                
                print(f"✅ Image: {jpg_filename} updated.")

            # ---------------------------
            # PART 2: GENERATE HTML (Only if missing)
            # ---------------------------
            html_filename = base_name + ".html"
            
            if not os.path.exists(html_filename):
                # The template content
                html_content = """<div id="description">
    <h3>Drawing Title</h3>
    <p>Description</p>
</div>"""
                
                with open(html_filename, "w", encoding="utf-8") as f:
                    f.write(html_content)
                
                print(f"   📄 HTML: {html_filename} created.")
            else:
                print(f"   ⏭️  HTML: {html_filename} exists (Skipped).")

        except Exception as e:
            print(f"❌ Error processing {filename}: {e}")

    print("\nAll done!")

if __name__ == "__main__":
    process_gifs()