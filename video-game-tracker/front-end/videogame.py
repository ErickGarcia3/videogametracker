import requests

# API Configuration
BASE_URL = "http://localhost:5000/api/"


def display_menu():
    """Display the main menu"""
    print("\n" + "=" * 50)
    print("PRODUCT MANAGEMENT SYSTEM".center(50))
    print("=" * 50)
    print("1. List All Game")
    print("2. Filter Game Details")
    print("3. Add New Game")
    print("4. Update Play status")
    print("5. Delete Game")
    print("6. Rate Game")
    print("7. Log Play Time")
    print("8. Exit")
    print("=" * 50)


def list_games():
    """List all games"""
    try:
        response = requests.get(f"{BASE_URL}/games")
        if response.status_code == 200:
            games = response.json()
            if not games:
                print("\nNo games found!")
                return

            print("\n" + "-" * 70)
            print(f"{'ID':<5}{'Title':<30}{'Platform':<15}{'Play_status':<20}{'Hours_played':<20}{'Rating':<20}{'Store_url':<20}")
            print("-" * 70)
            for game in games:
                print(
                    f"{game['id']:<5}{game['title']:<30}{game['platform']:<14}{game['play_status']:<20}{game['hours_played']:<20}{game['rating']:<20}{game['store_url']:<20}")
            print("-" * 70)
        else:
            print(f"\nError fetching products: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")


def view_games_filtered():
    """View games filtered by platform or status"""
    print("\nFilter by:")
    print("1. Platform (Pc/Android/IOS)")
    print("2. Status (Unplayed/Playing/Completed/Abandoned)")
    choice = input("Enter choice (1 or 2): ")

    if choice == "1":
        platform = input("Enter platform (Pc/Android/IOS): ").strip().lower()
        if platform not in ["pc", "android","ios"]:
            print("\nInvalid platform.")
            return
        filter_type = "platform"
        filter_value = platform
    elif choice == "2":
        play_status = input("Enter status (Unplayed/Playing/Completed/Abandoned): ").strip().lower()
        if play_status not in ["unplayed", "playing","completed","abandoned"]:
            print("\nInvalid status.")
            return
        filter_type = "play_status"
        filter_value = play_status
    else:
        print("\nInvalid choice.")
        return

    try:
        response = requests.get(f"{BASE_URL}/games", params={filter_type: filter_value})
        if response.status_code == 200:
            games = response.json()
            if not games:
                print(f"\nNo games found with {filter_type}: {filter_value}")
                return

            print("\n" + "-" * 50)
            print(f"GAMES FILTERED BY {filter_type.upper()}: {filter_value.upper()}".center(50))
            print("-" * 50)
            for game in games:
                if game.get(filter_type, "").lower() == filter_value:
                    print(f"ID: {game['id']}")
                    print(f"Title: {game['title']}")
                    print(f"Platform: {game.get('platform', 'N/A')}")
                    print(f"Play status: {game.get('play_status', 'N/A')}")
                    print(f"Hours played: {float(game['hours_played']):.2f}")
                    print(f"Rating: {float(game['rating']):.2f}")
                    print(f"Store_url: {game['store_url']}")
                    print("-" * 50)
                
        else:
            print(f"\nError: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")

def add_game():
    """Add a new game"""
    print("\nEnter game details:")
    title = input("Title: ")
    platform = input("Plaform (Pc/Android/IOS): ")
    play_status = input("Play Status (Unplayed/Playing/Completed/Abandoned): ")
    hours_played = input("Hours Played: ")
    rating = input("Rating (1-5): ")
    store_url = input("Store URL: ")

    if not title or not platform or not play_status or not hours_played or not rating or not store_url:
        print("\nTitle and platform, play status, hours played, rating and store URL are required!")
        return
    
    try:
        hours_played = float(hours_played)
    except ValueError:
        print("\nHours played must be a number!")
        return
    
    try:
        rating = float(rating)
        if not(rating<=1 or rating >=5):
           print("The rating must be between 1 and 5")
    except ValueError:
        print("\nRating must be a number!")
        return

    game_data = {
        "title": title,
        "platform": platform,
        "play_status": play_status,
        "hours_played": hours_played,
        "rating": rating,
        "store_url": store_url
    }

    try:
        response = requests.post(f"{BASE_URL}/games", json=game_data)
        if response.status_code == 201:
            print("\nGame added successfully!")
            new_game = response.json()
            print(f"New Game ID: {new_game['id']}")
        else:
            print(f"\nError adding product: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")


def update_game():
    """Update the play status of an existing game"""
    game_id = input("\nEnter game ID to update: ")

    # First get the current product details
    try:
        response = requests.get(f"{BASE_URL}/games/{game_id}")
        if response.status_code != 200:
            print(f"\nError: {response.text if response.status_code != 404 else 'Game not found!'}")
            return

        current_game = response.json()
        print("\nCurrent game details:")
        print(f"1. Title: {current_game['title']}")
        print(f"2. Platform: {current_game['platform']}")
        print(f"3. Play Status: {current_game['play_status']}")
        print(f"4. Hours Played: {current_game['hours_played']}")
        print(f"5. Rating: {current_game['rating']}")
        print(f"6. Store URL: {current_game['store_url']}")
        print("\nEnter new values (leave blank to keep current):")
        updates = {}

        play_status = input("New status of the game: ").strip().capitalize()
        if play_status in ["Unplayed", "Playing", "Complete", "Abandoned"]: 
            try:
               updates["play_status"] = play_status
            except ValueError:
                print("Play status must be in the choices!")
                return
               

        if not updates:
            print("\nNo changes made!")
            return

        try:
            response = requests.put(f"{BASE_URL}/games/{game_id}", json=updates)
            if response.status_code == 200:
                print("\nGame status updated successfully!")
            else:
                print(f"\nError updating game: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"\nConnection error: {e}")

    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")


def delete_game():
    """Delete a game"""
    game_id = input("\nEnter game ID to delete: ")
    confirm = input(f"Are you sure you want to delete product {game_id}? (y/n): ")

    if confirm.lower() != 'y':
        print("Deletion cancelled.")
        return

    try:
        response = requests.delete(f"{BASE_URL}/games/{game_id}")
        if response.status_code == 200:
            print("\nGame deleted successfully!")
        else:
            print(f"\nError deleting product: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")

def rate_game():
    """Rate an existing game"""
    game_id = input("\nEnter game ID to rate: ")

    # First get the current product details
    try:
        response = requests.get(f"{BASE_URL}/games/{game_id}")
        if response.status_code != 200:
            print(f"\nError: {response.text if response.status_code != 404 else 'Game not found!'}")
            return

        current_game = response.json()
        print("\nCurrent game details:")
        print(f"1. Title: {current_game['title']}")
        print(f"1. Platform: {current_game['platform']}")
        print(f"1. Play Status: {current_game['play_status']}")
        print(f"1. Hours Played: {current_game['hours_played']}")
        print(f"1. Rating: {current_game['rating']}")
        print(f"1. Store URL: {current_game['store_url']}")
        print("\nEnter new values (leave blank to keep current):")
        updates = {}
               

        rating = input("Rate game (1-5): ")
        if rating:
            try:
                rating = float(rating)
                if rating < 1 or rating > 5:
                    print("Rate must be between 1 and 5")
                updates["rating"] = rating    
            except ValueError:
                print("Price must be a number!")
                return


        if not updates:
            print("\nNo changes made!")
            return

        try:
            response = requests.put(f"{BASE_URL}/games/{game_id}", json=updates)
            if response.status_code == 200:
                print("\nGame status updated successfully!")
            else:
                print(f"\nError updating game: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"\nConnection error: {e}")

    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")

def Log_playtime():
    """Log play time of an existing game"""
    game_id = input("\nEnter game ID to update: ")

    # First get the current product details
    try:
        response = requests.get(f"{BASE_URL}/games/{game_id}")
        if response.status_code != 200:
            print(f"\nError: {response.text if response.status_code != 404 else 'Game not found!'}")
            return

        current_game = response.json()
        print("\nCurrent game details:")
        print(f"1. Title: {current_game['title']}")
        print(f"1. Platform: {current_game['platform']}")
        print(f"1. Play Status: {current_game['play_status']}")
        print(f"1. Hours Played: {current_game['hours_played']}")
        print(f"1. Rating: {current_game['rating']}")
        print(f"1. Store URL: {current_game['store_url']}")
        print("\nEnter new values (leave blank to keep current):")
        updates = {}

        hours_played = input("Log play time: ")
        if hours_played:
            try:
                updates["hours_played"] = float(hours_played)
            except ValueError:
                print("Log play time must be a number!")
                return


        if not updates:
            print("\nNo changes made!")
            return

        try:
            response = requests.put(f"{BASE_URL}/games/{game_id}", json=updates)
            if response.status_code == 200:
                print("\nGame status updated successfully!")
            else:
                print(f"\nError updating game: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"\nConnection error: {e}")

    except requests.exceptions.RequestException as e:
        print(f"\nConnection error: {e}")


def main():
    """Main program loop"""
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-6): ")

        if choice == '1':
            list_games()
        elif choice == '2':
            view_games_filtered()
        elif choice == '3':
            add_game()
        elif choice == '4':
            update_game()
        elif choice == '5':
            delete_game()
        elif choice == '6':
            rate_game()
        elif choice == '7':
            Log_playtime()
        elif choice == '8':
            print("\nExiting program. Goodbye!")
            break
        else:
            print("\nInvalid choice! Please enter a number between 1-6.")

        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()