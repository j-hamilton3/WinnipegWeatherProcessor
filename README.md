[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/LvdQZzDp)
This is an example file for you to include in your project.
You must have a title, a project description and a pylint section in this file. There are also other sections you should consider to have. *Make it professional.*

# Weather Processing App

## Project Description
```
Course: ADEV-3005 Programming in Python
Instructor:
Section Number:
Author:
Date Created:
Credit: 
Updates:
```
Expand the Project Introduction to include a detailed description of what the project does, its purpose, and who it's for. Highlight any unique features or challenges addressed by the project.

## Optional sections to include

**Installation**: Provide step-by-step instructions on how to install and set up the project. Include any prerequisites, such as Python version or external libraries, and how to install them.

**Usage**: Explain how to use the application, including command-line arguments, configuration files, and examples of common use cases. Screenshots or GIFs can be very helpful here.

**Technologies Used**: List the programming languages, frameworks, libraries, and any other technologies used in the project. This is helpful for understanding the project's technical stack and for users looking to learn from your code.

**Features**: Outline the key features of your application. This section can highlight what makes your project stand out.

**Acknowledgments**: A section to give thanks to individuals, organizations, or resources that contributed to the success of the project. This can include sources of inspiration, financial support, or technical guidance.

**Contact Information**: Provide details on how to reach the authors or maintainers for further questions or discussions about the project.

**Frequently Asked Questions (FAQs)**: Address common questions about the project. This can save time for both the project team and users.

**Known Issues and Limitations**: Document any known bugs or limitations in the current version of the project. This transparency can help manage user expectations and encourage contributions to resolve these issues.

**Future Work**: Briefly describe any planned enhancements or features for future releases. This shows that the project is active and continually improving.


### Pylint Result
************* Module weather_gui
weather_gui.py:12:0: E0401: Unable to import 'dateutil.relativedelta' (import-error)
weather_gui.py:11:0: W0611: Unused timedelta imported from datetime (unused-import)
weather_gui.py:12:0: W0611: Unused relativedelta imported from dateutil.relativedelta (unused-import)
************* Module weather_processor
weather_processor.py:10:0: E0401: Unable to import 'dateutil.relativedelta' (import-error)
weather_processor.py:11:0: E0401: Unable to import 'hypercli' (import-error)
weather_processor.py:32:12: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
************* Module scrape_weather
scrape_weather.py:79:4: R1705: Unnecessary "else" after "return", remove the "else" and de-indent the code inside it (no-else-return)
************* Module plot_operations
plot_operations.py:10:0: E0401: Unable to import 'matplotlib.pyplot' (import-error)
plot_operations.py:1:0: R0801: Similar lines in 2 files
==weather_gui:[47:85]
==weather_processor:[115:149]
    current_year = datetime.now().year

    valid_starting_year = False
    valid_end_year = False

    while not valid_starting_year:
        try:
            starting_year = int(input(f"Please enter a starting year" \
                                    f" (between 1996-{current_year}): "))
            if 1996 <= starting_year <= current_year:
                valid_starting_year = True
            else:
                print(f"Error: Please enter a year between 1996 and {current_year}.")
        except ValueError:
            print("Invalid input. Please enter a valid year.")

    while not valid_end_year:
        try:
            end_year = int(input(f"Please enter an end year (between 1996-{current_year}): "))
            if 1996 <= end_year <= current_year and end_year >= starting_year:
                valid_end_year = True
            else:
                print(f"Error: Please enter a year between 1996 and {current_year}" \
                    f" that is not less than the starting year.")
        except ValueError:
            print("Invalid input. Please enter a valid year.")

    # Generate the plot.
    plot = PlotOperations()
    plot.plot_temperature_boxplots(starting_year, end_year)

    print("Box plot successfully generated.")
    print()
    input("Press enter to exit...")

def display_line_plot():
    """Generates a line graph of weather data based on user input."""
    # Get the current year from datetime. (duplicate-code)
plot_operations.py:1:0: R0801: Similar lines in 2 files
==weather_gui:[85:110]
==weather_processor:[155:181]
        current_year = datetime.now().year

        valid_year = False
        valid_month = False

        while not valid_year:
            try:
                year = int(input(f"Please enter a year (between 1996-{current_year}): "))
                if 1996 <= year <= current_year:
                    valid_year = True
                else:
                    print(f"Error: Please enter a year between 1996 and {current_year}.")
            except ValueError:
                print("Invalid input. Please enter a valid year.")

        while not valid_month:
            try:
                month = int(input("Please enter a month (between 1-12): "))
                if 1 <= month <= 12:
                    valid_month = True
                else:
                    print("Error: Please enter a month between 1 and 12.")
            except ValueError:
                print("Invalid input. Please enter a valid month.")

        # Generate the plot. (duplicate-code)
plot_operations.py:1:0: R0801: Similar lines in 2 files
==weather_gui:[35:47]
==weather_processor:[102:109]
        print("Fetching weather data...")
        weather_data = fetch_weather_data()
        db = DBOperations()
        db.save_data(weather_data)
        print("Weather data successfully updated. :)")
        print()
        input("Press enter to exit...") (duplicate-code)
plot_operations.py:1:0: R0801: Similar lines in 2 files
==weather_gui:[20:27]
==weather_processor:[84:91]
    weather_processor = WeatherProcessor()
    update_dates_return = weather_processor.update_dates()

    if not update_dates_return :
        print("There is no new data available. You are up to date!")
        print()
        input("Press enter to exit...") (duplicate-code)
plot_operations.py:1:0: R0801: Similar lines in 2 files
==weather_gui:[27:35]
==weather_processor:[92:97]
        else:
            weather_processor.update_data()
            print("Weather data successfully updated. :)")
            print()
            input("Press enter to exit...") (duplicate-code)

-----------------------------------
Your code has been rated at 9.28/10

