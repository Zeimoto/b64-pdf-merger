import base64
from PyPDF2 import PdfMerger, PdfReader
import os
import io

folderpath = "docs/"
files = []

print("Opening files in docs/")
for filename in os.listdir(folderpath):
    if filename.endswith("txt"):
        files.append(filename)
        print("º", filename)    

# Sorting by ascending order
files.sort()
print("Sorted:", files)

merger = PdfMerger()

for filename in files:
    filepath = os.path.join(folderpath, filename)
    with open(filepath, "r") as f:
        # Read the base64 encoded content
        base64_content = f.read()
        # Decode the base64 content to bytes
        try:
            pdf_bytes = base64.b64decode(base64_content)
        except base64.binascii.Error as e:
            print(f"Error decoding base64 content from {filename}: {e}")
            continue

        # Use BytesIO to treat the bytes as a file-like object
        pdf_stream = io.BytesIO(pdf_bytes)
        
        # Print debugging information
        print(filename)
        print(pdf_stream)
        
        # Check if the decoded content is a valid PDF
        try:
            PdfReader(pdf_stream)
            pdf_stream.seek(0)  # Reset stream position after validation
            merger.append(pdf_stream)
        except Exception as e:
            print(f"Error validating PDF content from {filename}: {e}")
            continue

# Output the merged PDF to a BytesIO stream
output_pdf_stream = io.BytesIO()
merger.write(output_pdf_stream)
merger.close()

# Reset the stream position to the beginning
output_pdf_stream.seek(0)

# Encode the merged PDF to base64
merged_pdf_base64 = base64.b64encode(output_pdf_stream.read()).decode('utf-8')

# Save the merged PDF to a file
output_pdf_path = os.path.join(folderpath, "merged_result.pdf")
with open(output_pdf_path, "wb") as f:
    f.write(output_pdf_stream.getbuffer())

# Save the merged base64 to a file
output_b64_path = os.path.join(folderpath, "merged_b64_result.txt")
with open(output_b64_path, "w") as f:
    f.write(merged_pdf_base64)

# Output the paths and base64 content
print(f"Merged PDF created at: {output_pdf_path}")
print(f"Base64 encoded merged PDF saved at: {output_b64_path}")
