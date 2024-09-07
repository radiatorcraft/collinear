import json
import scratchapi
import time
import os
import datetime
import random
import logging

def load_settings_from_json(filename):
    try:
        with open(filename, 'r') as f:
            settings = json.load(f)
            return settings
    except FileNotFoundError:
        print(f"Error: Settings file '{filename}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None

def save_settings_to_json(filename, settings):
    try:
        with open(filename, 'w') as f:
            json.dump(settings, f, indent=4)
    except Exception as e:
        logging.error(f"Error saving settings to JSON: {e}")

def follow_users_from_file(filename, username, password, cycle_time, log_interval_time, log_interval_cycles, log_path, settings_path, start_user=None):

    total_cycles = 0
    cycles_per_hour = 0.0
    start_time = time.time()
    log_time = time.time()
    log_cycle = 0
    found_start_user = False

    try:
        scratch = scratchapi.ScratchUserSession(username, password)

        if not scratch.tools.verify_session():
            print("Invalid credentials. Please check your username and password.")
            return

       
        script_start_time = datetime.datetime.now()
        formatted_start_time = script_start_time.strftime("%I:%M %p, %B %d, %Y")
        with open(log_path, "a") as log_file:
            log_file.write("\n")  
            log_file.write(f"SCRIPT STARTED - {formatted_start_time}\n")
            log_file.write(f"Cycle Time: {cycle_time}s\n")
            log_file.write(f"Log Interval Time: {log_interval_time}m\n")
            log_file.write(f"Log Interval Cycles: {log_interval_cycles}\n")
            log_file.write("\n")  

        
        with open(filename, 'r') as file:
            lines = len(file.readlines())

        
        start_index = 0
        if start_user:
            with open(filename, 'r') as file:
                for i, line in enumerate(file):
                    if line.strip() == start_user:
                        start_index = i + 1
                        break

        with open(filename, 'r') as file:
            for i, line in enumerate(file):
                if i < start_index:
                    continue

                user_to_follow = line.strip()

                try:
                    scratch.users.follow(user_to_follow)
                    print(f"Attempted to follow: {user_to_follow}")
                    total_cycles += 1
                    time.sleep(cycle_time)

                    
                    os.system('cls' if os.name == 'nt' else 'clear') 

                    print(f"Attempted cycles: {total_cycles}")

                    
                    if total_cycles > 0:
                        cycles_per_hour = total_cycles / (time.time() - start_time) * 3600
                        print(f"Estimated cycles per hour: {cycles_per_hour:.2f}")

                    
                    remaining_lines = lines - i - 1
                    estimated_remaining_time = remaining_lines / (total_cycles / (time.time() - start_time))

                    
                    if estimated_remaining_time >= 3600:
                        estimated_remaining_time /= 3600
                        time_unit = "hours"
                    elif estimated_remaining_time >= 60:
                        estimated_remaining_time /= 60
                        time_unit = "minutes"
                    else:
                        time_unit = "seconds"

                    print(f"Estimated remaining time: {estimated_remaining_time:.2f} {time_unit}")

                    
                    log_cycle += 1
                    if log_interval_time > 0 and time.time() - log_time >= log_interval_time * 60:
                        log_time = time.time()
                        log_cycle = 0 
                    if log_interval_cycles > 0 and log_cycle >= log_interval_cycles:
                        log_cycle = 0
                        timestamp = datetime.datetime.now()
                        formatted_timestamp = timestamp.strftime("%I:%M %p, %B %d, %Y")
                        current_runtime = time.time() - start_time
                        with open(log_path, "a") as log_file:
                            log_file.write(f"{formatted_timestamp} - Cycles: {total_cycles}, Cycles/hour: {cycles_per_hour:.2f}, Runtime: {current_runtime:.2f}s, Current Follow: {user_to_follow}, Estimated Remaining Time: {estimated_remaining_time:.2f} {time_unit}\n")

                except scratchapi.ScratchAPIException as e:
                    print(f"Couldn't follow '{user_to_follow}': {e}")

    except FileNotFoundError as e:
        print(f"Error: File '{filename}' not found.")

def benchmark(filename, username, password, cycle_time, log_path):
    
    try:
        scratch = scratchapi.ScratchUserSession(username, password)

        if not scratch.tools.verify_session():
            print("Invalid credentials. Please check your username and password.")
            return

        with open(filename, 'r') as f:
            lines = f.readlines()

        
        buffer_usernames = random.sample(lines, 10)

        
        load_start = time.time()
        remaining_usernames = random.sample(list(set(lines) - set(buffer_usernames)), 50)
        load_end = time.time()
        load_time = load_end - load_start

        
        buffer_start = time.time()
        for user in buffer_usernames:
            user_to_follow = user.strip()
            try:
                scratch.users.follow(user_to_follow)
            except scratchapi.ScratchAPIException as e:
                print(f"Couldn't follow '{user_to_follow}': {e}")
        buffer_end = time.time()
        buffer_time = buffer_end - buffer_start
        buffer_time_per_user = buffer_time / len(buffer_usernames)

        
        estimated_time = buffer_time_per_user * len(remaining_usernames)

       
        main_start = time.time()
        for user in remaining_usernames:
            user_to_follow = user.strip()
            try:
                scratch.users.follow(user_to_follow)
            except scratchapi.ScratchAPIException as e:
                print(f"Couldn't follow '{user_to_follow}': {e}")
        main_end = time.time()
        main_time = main_end - main_start
        main_time_per_user = main_time / len(remaining_usernames)

        
        with open(log_path, "a") as log_file:
            log_file.write("\nBenchmark Results:\n")
            log_file.write(f"Buffer load time: {load_time:.2f} seconds\n")
            log_file.write(f"Buffer processing time: {buffer_time:.2f} seconds\n")
            log_file.write(f"Estimated time: {estimated_time:.2f} seconds\n")
            log_file.write(f"Main processing time: {main_time:.2f} seconds\n")
            log_file.write(f"Buffer time per user: {buffer_time_per_user:.2f} seconds\n")
            log_file.write(f"Main time per user: {main_time_per_user:.2f} seconds\n")

    except FileNotFoundError as e:
        print(f"Error: File '{filename}' not found.")



if __name__ == "__main__":
    log_path = '' #path to your desired log location goes here
    settings_path = "" # path to settings.json goes here
    username = '' #your username for your scratch account goes here
    password = '' # your scratch account password goes here
    filename = '' #username list goes here
    error_path ='' #error path goes here 
    
    logging.basicConfig(filename=error_path, level=logging.ERROR)

    settings = load_settings_from_json(settings_path)

    choice = input("Choose an option: 1. Load settings, 2. Start script, 3. Benchmark: ")

    if choice == "1":
        if not settings:
            print("Settings file not found.")
            exit()
        cycle_time = settings["cycle_time"]
        log_interval_time = settings["log_interval_time"]
        log_interval_cycles = settings["log_interval_cycles"]
        start_user = settings.get("start_user")
    elif choice == "2":
        cycle_time = int(input("Enter time between cycles in seconds: "))
        log_interval_time = int(input("Enter log interval in minutes (0 to disable): "))
        log_interval_cycles = input("Enter log interval in cycles (0 or N to disable): ")
        if log_interval_cycles.upper() == 'N':
            log_interval_cycles = 0
        else:
            log_interval_cycles = int(log_interval_cycles)

        start_user = input("Enter username to start from (press Enter or 0 to start from beginning): ")
        if start_user == '':
            start_user = None

        save_settings = input("Save settings to JSON? (y/n): ")
        if save_settings.lower() == "y":
            settings_data = {
                "cycle_time": cycle_time,
                "log_interval_time": log_interval_time,
                "log_interval_cycles": log_interval_cycles,
                "start_user": start_user
            }
            save_settings_to_json(settings_path, settings_data)

    elif choice == "3":
        
        cycle_time = 60  
        benchmark(filename, username, password, cycle_time, log_path)
    else:
        print("Invalid choice.")



    start_time = time.time()  
    follow_users_from_file(filename, username, password, cycle_time, log_interval_time, log_interval_cycles, log_path, settings_path, start_user)
