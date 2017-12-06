from html.parser import HTMLParser

"""
Classs used to detect starting and closing tags as well as extract the 
name of the tag given a line of html
"""
class MyHTMLParser(HTMLParser):
    def __init__(self):
    	super().__init__()
    	self.startTags = []
    	self.endTags = []

    def handle_starttag(self, tag, attrs):
        self.startTags.append(tag)

    def handle_endtag(self, tag):
        self.endTags.append(tag)

    def hasStartTags(self):
        return self.startTags != []

    def hasEndTags(self):
        return self.endTags != []

    def hasData(self):
        return self.Data != ""

    def getStartTags(self):
        return self.startTags

    def getEndTags(self):
        return self.endTags



"""
Given a string of HTML, a dictionary for the designated colors of each tag, and a list of tags that have no closing tag return
a string of HTML with corresponding color commands inserted infront of each tag where required.
"""
def colorize(html, colors, unclosedTags):
	result = ""
	parser = MyHTMLParser()
	stack = []
	current_color = ""

	# Loop through each line of the html
	for line in html.split("\n"):
		if line != "\n":
			parser.feed(line)
			all_open_tags = []
			all_close_tags = []

			# Append all start tags 
			if parser.hasStartTags():
				all_open_tags = parser.getStartTags()

			# Append all closing tags 
			if parser.hasEndTags():
				all_close_tags = parser.getEndTags()

			# if all_open_tags and all_close_tags is empty pop from stack and add color cmnd
			if len(all_open_tags) == 0 and len(all_close_tags) == 0:
				if len(stack) > 0 and current_color != stack[0]:
					stack_color = stack[0]
					current_color = stack_color
					result += "\color["+stack_color+"]"+line
				else:
					result += line
			else:
				#Loop through each character of the line
				for i in range(len(line)):
					# Append the color command with corresponding color if this is an opening tag
					if is_open_tag(i, line):
						next_tag = all_open_tags.pop(0)
						try:
							current_color = colors[next_tag.lower()]
						except KeyError:
							print("Error: The tag '"+next_tag+"'' could not be found in the 'colors' \
								dictionary, please add it under the __main__ method.")
						result += "\color["+current_color+"]"
						# Only append color to stack if this tag has a closing tag
						if next_tag.lower() not in unclosedTags:
							stack.insert(0, current_color)

					# If closing tag pop the color from stack 
					elif is_close_tag(i, line):
						stack_color = stack.pop(0)
						all_close_tags.pop(0)
						# Only add color command if the stack color and current color dont align
						if stack_color != current_color:
							result += "\color["+stack_color+"]"
							current_color = stack_color

					result += line[i]
			result += "\n"

	return result


"""
Method used to detect if index of current character is part of an opening tag
"""
def is_open_tag(indx, line):
	if indx < len(line) and line[indx] == '<' and line[indx+1] != "/":
		return True
	return False

"""
Method used to detect if index of current character is part of an closing tag
"""
def is_close_tag(indx, line):
	if indx < len(line) and line[indx] == '<' and line[indx+1] == '/':
		return True
	return False


if __name__ == "__main__":

	with open('input.html', 'r') as myfile:
		html = myfile.read()

	# A list of common html tags with a corresponding color, Please add more if a color is not found. Note that the keys must be lowercase
	colors = {"html":"RED","body":"TURQUOISE","title":"GREEN","head":"YELLOW","br":"PINK","h1":"DARKGREEN","p":"DARKGRAY", "a":"BLUE"}
	unclosedTags = ["area", "base", "br", "col", "command", "embed", "hr", "img", "input", "keygen", "link", "meta", "param", "source", "track", "wbr"] 
	result = colorize(html, colors, unclosedTags)

	text_file = open("output.html", "w")
	text_file.write(result)
	text_file.close()
