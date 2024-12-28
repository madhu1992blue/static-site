
import generator
import os
def main():
    generator.removeRecurse("public")
    os.mkdir("public")
    generator.copy("static","public")

    generator.generate_pages_recursive("content","template.html", "public")

if __name__ == "__main__":
    main()
    
    
