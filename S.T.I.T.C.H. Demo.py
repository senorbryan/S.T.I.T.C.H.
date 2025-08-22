import json
from pathlib import Path
from PIL import Image, ImageDraw

#Greets the user
def greet():
    while(True):
        print("WELCOME to S.T.I.T.C.H. This program serves as an interface to CREATE blueprint designs for clothing.")
        print("Please select an option below.")
        print("1. Start a NEW blueprint")
        print("2. Open an EXISTING project")
        print("3. Exit")
        choice = str(input())

        if choice.isdigit():
            if (choice == '1'):
                return 1
            
            elif (choice == '2'):
                return 2
            
            elif (choice == '3'):
                return False
            
        if (choice.lower() == 'start a new blueprint'):
            return 1

        elif (choice.lower() == 'open a project'):
            return 2

        print()
        print("You did not select a PROPER option. Please try again.")

#Presents the user with a list of garments to select from, which will provide a starting design to edit
def articles():
    print()

    while (True):
        print("What article of CLOTHING would you like to print?")
        for i, garment in enumerate(garments, 1):
            print(f"{i}. {garment.title()}")
        choice = input()
        
        if (choice.lower() in garments):
            index = garments.index[garment]
            return index
        
        if choice.isdigit():
            return int(choice)

        else:
            print()
            print("You did not select a PROPER option. Please try again.")

#Presents the user with a list of editorial features for their clothing blueprint
def features():
    while (True):
        print()
        print("What would you like to do with your current design?")
        print("1. CHANGE background color")
        print("2. FILL the panel")
        print("3. SAVE Current Project")
        print("4. RENAME Current Project")
        print("5. Exit")
        choice = input()

        if (choice.lower() == "change background color" or choice == "1"):
            return 1
        
        elif (choice.lower() == "fill" or choice == "2"):
            return 2
        
        elif (choice.lower() == "save current project" or choice == "3"):
            return 3
        
        elif (choice.lower() == 'rename' or choice == '4'):
            return 4

        elif (choice.lower() == 'exit' or choice == '5'):
            return 5
        
        else:
            print("You did not select a PROPER option. Please try again.")

#Presents the user with a list of panels necessary[Currently only works for boxer shorts]
def panels(garment):
    if garment == "Boxers":
        while (True):
            print()
            print("What KIND of panel are you looking to design?")
            print("1. Leg Panel")
            panel = input()

            if panel.isdigit():
                if panel == '1':
                    return "Leg Panel"
            
            if (panel.lower() == "leg panel"):
                return "Leg Panel"
            
            else:
                print()
                print("You did not select a PROPER option. The fill option has been CANCELLED.")
            
#Presents the user with all .jpg files that can be used to fill their panels
def load_designs():
    directory = Path(__file__).parent
    designs_folder = directory / "Designs"
    designs = []

    for design in designs_folder.iterdir():
        if design.is_file():
            designs.append(design)

    if not designs:
        print()
        print("No available designs could be FOUND. To apply any designs, ADD them to your 'Designs' folder.")
        return None
    
    print()
    print("Which DESIGN would you like to use?")

    for i, design in enumerate(designs, 1):
        print(f"{i}. {design.stem}")

    select = input()

    if select.isdigit():
        index = int(select) - 1
        if 0 <= index < len(designs):
            design = designs[index]
            return design
        
    for design in designs:
        if select.lower() == design.stem.lower():
            return design
        
    print(f"{select} is NOT select a valid choice.")
    return None

#Saves the current project
def save(image, project, garment, panel, width, background, design):
    directory = Path(__file__).parent / "Projects"
    folder = directory / garment / panel
    folder.mkdir(parents = True, exist_ok = True)

    file = (f"{project} {panel}.jpg")
    metadata = (f"{project} {panel}.json")
    image_path = folder / file
    metadata_path = folder / metadata
    design_path = str(design)
    measurements = {"width": width, "design" : design_path, "background" : background, "garment" : garment, "panel" : panel}

    image.save(image_path)

    with open(metadata_path, "w") as file:
        json.dump(measurements, file, indent = 1)

    print()
    print(f"The project {image_path} was SUCCESSFULLY saved.")

#Renames the current project
def rename():
    print()
    print(f"The CURRENT name of your project is {draft}. What would you like to CHANGE it to?")
    overwrite = input()

    print()
    print(f"The current name of your project has been RENAMED to {overwrite}.")

    return overwrite

#Changes the color 
def change_background():
    print()
    print("Pick a background color:")

    for i, color in enumerate(colors , start = 1):
        print(f"{i:1}. {color}")
    background = input().lower()

    if background.isdigit():
        background = colors[int(background) - 1]
    
    elif (background in colors):
        pass
        
    else:
        print()
        print("You did not select a PROPER option. The background color was set to WHITE.")
        return "white"

    return background

#Creates the measurements for garments
def measure(garment):
    if garment == "Boxers":
        while (True):
            print()
            print(f"What is the WAIST size in INCHES for the person wearing the {garment}?")
            size = input()

            if not (size.isdigit()):
                print()
                print("You did not input a proper SIZE in inches. Please try again.")
            
            else:
                inches = int(size)
                ease = 2
                seam_allowance = 1
                width = (inches / 2) + ease + seam_allowance

                return float(width)

#Retrieves projects to work on
def retrieve():
    #Pathing for type of garment (e.g. Shirts, Pants, etc.)
    directory = Path(__file__).parent / "Projects"
    clothing = []
    garment = ""

    for folder in directory.iterdir():
        if folder.is_dir():
            clothing.append(folder.name)

    if not (clothing or directory.exists()):
        print()
        print("You don't seem to have ANY saved projects. Returning to MAIN menu.")
        return

    print()
    print("What GARMENT type is your project?")

    for i, cloth in enumerate(clothing, 1):
        print(f"{i}. {cloth}")
    choice = input()

    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(clothing):
            garment = clothing[index]
        
    for cloth in clothing:
        if cloth.lower() == choice.lower():
            garment = cloth

    #Pathing for type of garment panel (e.g. Sleeve Panel, Leg Panel, etc.)
    if (garment):
        panel = ""
        articles_dir = Path(__file__).parent / "Projects"/ garment
        articles = []

        for article in articles_dir.iterdir():
            if article.is_dir():
                articles.append(article.name)
            
        if not (articles or articles_dir.exists()):
            print()
            print(f"You don't seem to have ANY saved {garment} projects. Returning to MAIN menu.")
            return

        print()
        print(f"What PANEL would you like to retrieve for your {garment} project?")

        for i, article in enumerate(articles, 1):
            print(f"{i}. {article}")
        choice = input()

        if choice.isdigit():
            index = int(choice) - 1
            if 0 <= index < len(articles):
                panel = articles[index]
            
        for article in articles:
            if article.lower() == choice.lower():
                panel = article
        
        #Pathing for clothing panel projects
        if (panel):
            projects_dir = Path(__file__).parent / "Projects" / garment / panel
            projects = []
            projects_path = []

            for project in projects_dir.iterdir():
                if project.is_file() and project.suffix.lower() != ".json":
                    projects.append(project.stem)
                    projects_path.append(project)
                
            if not (projects or projects_dir.exists()):
                print()
                print(f"You don't seem to have ANY saved {panel} for your {garment} projects. Returning to MAIN menu.")
                return

            print()
            print(f"What PROJECT would you like to retrieve?")

            for i, project in enumerate(projects, 1):
                print(f"{i}. {project}")
            choice = input()

            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(projects):
                    path = projects_path[index]
                    json_path = path.with_suffix(".json")

                    with open(json_path, "r") as file:
                        data = json.load(file)
                    
                    width = data.get("width")
                    background = data.get("background")
                    panel = data.get("panel")
                    design_path = Path(data["design"])

                    print()
                    print(f"You have SUCCESSFULLY retrieved the {projects[index]} project!")
                    return projects[index], path, width, background, design_path, garment, panel
                
            for project, project_path in zip(projects, projects_path):
                if project.lower() == choice.lower():
                    json_path = project_path.with_suffix(".json")

                    with open(json_path, "r") as file:
                        data = json.load(file)

                    width = data.get("width")
                    background = data.get("background")
                    panel = data.get("panel")
                    design_path = Path(data["design"])
                    garment = data.get("garment")

                    print()
                    print(f"You have SUCCESSFULLY retrieved the {project} project!")
                    return project, path, width, background, design_path, garment, panel

        print()
        print("You did not select a PROPER option. Returning to MAIN menu.")

#Draws a base shape for boxer shorts
def create_boxer_shorts_panel(draw: ImageDraw.ImageDraw, *, width) -> None:
    outline = "black"
    outline_w = 6
    waistline = [(80, 120),(405, 120)]
    size = (f"{width} in.")

    draw.polygon(boxer_panel_coordinates)
    draw.line(boxer_panel_coordinates + [boxer_panel_coordinates[0]], fill = outline, width = outline_w)

    x = (waistline[0][0] + waistline[1][0]) // 2
    y = waistline[0][1] - 20

    draw.text((x, y), size, fill = "black")

#Will fill the boxer shorts panel with a custom design chosen by the user
def fill_boxer_shorts_panel(image: Image.Image, fill = None, *,outline = "black", outline_w = 6, scale_factor = 0.35) -> None:
    draw = ImageDraw.Draw(image)

    #Condition if a design is already filling the panel
    if fill is not None:
        #Condition if the filling is a standard color
        if isinstance(fill, str) and fill.lower() in colors:
            draw = ImageDraw.Draw(image)
            draw.polygon([(80, 120),(405, 120), (405, 350), (460, 370), (460, 399), (460, 420), (40, 420), (40, 355), (80, 335)], fill = fill)
            
            return fill
        
        #Condition if the filling is from a reference image
        else:
            tile = Image.open(fill).convert("RGBA")
            new_width = int(tile.width * scale_factor)
            new_height = int(tile.height * scale_factor)
            tile = tile.resize((new_width, new_height))
            W, H = image.size
            pw, ph = tile.size

            tiled = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            for y in range(0, H, ph):
                for x in range(0, W, pw):
                    tiled.paste(tile, (x, y))

            mask = Image.new("L", (W, H), 0)
            ImageDraw.Draw(mask).polygon(boxer_panel_coordinates, fill=255)

            image.paste(tiled, (0, 0), mask)
            return fill

    print()
    print("Would you like to SUBMIT a reference image?")
    confirm = input()

    if (confirm.lower() == 'yes' or confirm.lower() == 'y'):
        design = load_designs()

        #Condition if no designs can be found
        if design is None:
            print()
            print("What color would you like to fill the panel with?")
            for i, color in enumerate(colors, 1):
                print(f"{i}. {color.title()}")
            choice = input()

            if choice in colors:
                fill = choice
            
            elif choice.isdigit() and 1 <= int(choice) <= len(colors):
                fill = colors[int(choice) - 1]
                
            else:
                print("You did not select a PROPER option. The fill option has been CANCELLED.")
                return
            
            draw.polygon(boxer_panel_coordinates, fill = fill)
            return
        
        #Condition if designs were found
        else:
            tile = Image.open(design).convert("RGBA")
            new_width = int(tile.width * scale_factor)
            new_height = int(tile.height * scale_factor)
            tile = tile.resize((new_width, new_height))
            W, H = image.size
            pw, ph = tile.size

            tiled = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            for y in range(0, H, ph):
                for x in range(0, W, pw):
                    tiled.paste(tile, (x, y))

            mask = Image.new("L", (W, H), 0)
            ImageDraw.Draw(mask).polygon(boxer_panel_coordinates, fill=255)

            image.paste(tiled, (0, 0), mask)
            return design

    #Condition if user wants to select a standard color to fill the panel    
    else:
        print()
        print("What color would you like to fill the panel with?")
        for i, color in enumerate(colors, 1):
            print(f"{i}. {color.title()}")
        choice = input()

        if choice in colors:
            solid_fill = choice
        
        elif choice.isdigit() and 1 <= int(choice) <= len(colors):
            solid_fill = colors[int(choice) - 1]
            
        else:
            print("You did not select a PROPER option. The fill option has been CANCELLED.")
            return
        
        draw.polygon(boxer_panel_coordinates, fill = solid_fill)

    draw.line(boxer_panel_coordinates + [boxer_panel_coordinates[0]], fill = outline, width = outline_w)

draft = ""
background = ""
exit = False
colors = ["red", "green", "blue", "yellow", "cyan", "magenta", "black", "white", "gray", "purple", "orange", "pink"]
shapes = ["rectangle", "circle", "triangle"]
garments = ["boxer shorts"]
boxer_panel_coordinates = [(80, 120),(405, 120), (405, 350), (460, 370), (460, 399), (460, 420), (40, 420), (40, 355), (80, 335)]

#S.T.I.T.C.H. Interface
while not (exit):
    choice = greet()

    #Condition if the user wants to create a new project
    if (choice == 1):
        article = articles()

        #Condition if the user wants to make a panel for boxers
        if (article == 1):
            GARMENT = "Boxers"

            print()
            print("Name your NEW project.")
            draft = input()

            panel = panels(GARMENT)

            #Condition if the user wants to make a leg panel
            if panel == "Leg Panel":
                background = "white"
                design = "white"
                width = measure(GARMENT)

                #Creates the base shape; Image object makes the background while the Draw image makes the shape and can fill it with a design
                image = Image.new("RGB", (500, 500), color = background)
                draw = ImageDraw.Draw(image)
                create_boxer_shorts_panel(draw, width = width)
                image.show()

                while not(exit):
                    choice = features()

                    #Condition if the user wants to change the background color
                    if (choice == 1):
                        background = change_background()
                        image = Image.new("RGB", (500, 500), color = background)
                        draw = ImageDraw.Draw(image)
                        create_boxer_shorts_panel(draw, width = width)
                        design = fill_boxer_shorts_panel(image, design)
                        
                    #Condition if the user wants to change filling of panel
                    elif (choice == 2):
                        design = fill_boxer_shorts_panel(image)

                    #Condition if the user wants to save the current project
                    elif (choice == 3):
                        print()
                        save(image, draft, GARMENT, panel, width, background, design)

                    #Condition if the user wants to rename the current project
                    elif (choice == 4):
                        draft = rename()

                    #Condition if the user wants to exit the program
                    elif (choice == 5):
                        print()
                        print("Would you like to SAVE your current project?")
                        choice = input()

                        if (choice.lower() == "no"):
                            print()
                            print("Thank YOU for using S.T.I.T.C.H. interface. Farewell!")
                            exit = True

                        else:
                            print()
                            save(image, draft, GARMENT, panel, width, background, design)
                            print("Thank YOU for using S.T.I.T.C.H. interface. Farewell!")
                            exit = True

                    else:
                        print()
                        print("You did not select a PROPER option. Please try again.")

                    image.show()

            else:
                print()
                print("You did not select a PROPER option. Please try again")
            
    #Condition if the user wants to open an existing project
    elif (choice == 2):
        draft, path, width, background, design, garment, panel = retrieve()

        if draft:
            image = Image.open(path)
            draw = ImageDraw.Draw(image)

            if (garment == "Boxers"):
                while not(exit):
                    choice = features()

                    #Condition if the user wants to change the background color
                    if (choice == 1):
                        background = change_background()
                        image = Image.new("RGB", (500, 500), color = background)
                        draw = ImageDraw.Draw(image)
                        create_boxer_shorts_panel(draw, width = width)
                        design = fill_boxer_shorts_panel(image, design)
                        
                    #Condition if the user wants to change filling of panel
                    elif (choice == 2):
                        design = fill_boxer_shorts_panel(image)

                    #Condition if the user wants to save the current project
                    elif (choice == 3):
                        print()
                        save(image, draft, GARMENT, panel, width, background, design)

                    #Condition if the user wants to rename the current project
                    elif (choice == 4):
                        draft = rename()

                    #Condition if the user wants to exit the program
                    elif (choice == 5):
                        print()
                        print("Would you like to SAVE your current project?")
                        choice = input()

                        if (choice.lower() == "no"):
                            print()
                            print("Thank YOU for using S.T.I.T.C.H. interface. Farewell!")
                            exit = True

                        else:
                            print()
                            save(image, draft, GARMENT, panel, width, background, design)
                            print("Thank YOU for using S.T.I.T.C.H. interface. Farewell!")
                            exit = True

                    else:
                        print()
                        print("You did not select a PROPER option. Please try again.")

                    image.show()
        else:
            pass

    else:
        print()
        print("You did not select a PROPER option. Please try again")

