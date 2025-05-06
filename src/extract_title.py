def extract_title(markdown):
  # Split the markdown into lines
  lines = markdown.split("\n")
    
  # Look through each line
  for line in lines:
      # Check if the line starts with a single # (not ## or ###)
      if line.startswith("# "):
          # Extract the title (everything after the # and any whitespace)
          return line[1:].strip()
    
  # If we get here, no h1 was found
  raise Exception("No h1 header found in markdown")