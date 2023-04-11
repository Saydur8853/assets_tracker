# AssetTrackr

a Django app to track corporate assets such as phones, tablets, laptops and other gears handed out to employees.

## Python version: 3.10

## Instructions to run the Project

1. Goto the directory where you want to store your project.
2. Clone the git repository to the project directory.
3. Open the terminal and navigate to the project directory from the terminal.
4. This project dependencies managed by PDM https://pdm.fming.dev
    * If you don't have `PDM` installed then install it by typing `pip install --user pdm`.
5. Install the project dependencies by typing `pdm sync` on the terminal.
6.Migrate the database by typing `pdm migrate` on the terminal.
7. Create admin user if you want by typing `pdm createsuperuser` and give the required credentials on the terminal.
8. Now, Run the project from your **localhost** by typing `pdm start`
9. Navigate to the URL [127.0.0.1:8000/api](127.0.0.1:8000/api) or [localhost:8000/api](localhost:8000/api) from your browser.
10. You can terminate the server anytime by **CTRL+c**.
