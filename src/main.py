from textnode import TextNode, TextType

def main():
	node = TextNode(TextType.BOLD, "This is a text node", "https://www.boot.dev")
	print(node)

if __name__ == "__main__":
    main()