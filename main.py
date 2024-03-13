import requests, threading

def check_plate_availability(plate):
    url = f"https://bmvonline.dps.ohio.gov/bmvonline/oplates/PlatePreview?plateNumber={plate}&vehicleClass=PC&organizationCode=0"
    response = requests.get(url)
    
    if "Plate is issued." in response.text:
        return False  
    elif "This plate number is currently available." in response.text:
        return True  
    else:
        return None

def process_plate(plate):
    is_available = check_plate_availability(plate)
    if is_available is True:
        print(f"plate {plate} is available!")
        return plate
    return None

def main():
    input_file = "plates.txt"

    with open(input_file, "r") as f:
        plates = f.read().splitlines()

    available_plates = []
    threads = []

    thread_count = int(input("threads: "))

    for plate in plates:
        thread = threading.Thread(target=lambda: available_plates.append(process_plate(plate)))
        thread.start()
        threads.append(thread)

        while threading.active_count() >= thread_count:
            pass

    for thread in threads:
        thread.join()

    available_plates = list(filter(None, available_plates))

    if available_plates:
        with open("plates-available.txt", "w") as output_file:
            output_file.write("\n".join(available_plates))
        print("available plates saved to 'plates-available.txt'")
    else:
        print("no available plates found.")

if __name__ == "__main__":
    main()
