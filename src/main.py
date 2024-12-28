
import generator
import os
def main():
    generator.removeRecurse("public")
    os.mkdir("public")
    generator.copy("static","public")

    generator.generate_page("content/index.md","template.html", "public/index.html")

if __name__ == "__main__":
    main()
    
    
