import subprocess
import time

def get_gpu_temperature():
    temp_info = subprocess.check_output(["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"], universal_newlines=True)
    return int(temp_info.strip())

def set_fan_speed(speed):
    for i in range(2):  # Assuming you have 2 fans
        subprocess.run(["sudo", "nvidia-settings", "-a", f"[gpu:0]/GPUFanControlState=1", "-a", f"[fan:{i}]/GPUTargetFanSpeed={speed}"])

def adjust_fan_curve():
    temp = get_gpu_temperature()
    if temp is None:
        print("Could not get GPU temperature")
        return

    if temp < 40:
        set_fan_speed(50)
    elif temp < 50:
        # Gradually raise fan speed from 50% to 60% as temperature increases from 40 to 50
        speed = 50 + 10 * ((temp - 40) / 10)
        set_fan_speed(int(speed))
    else:
        # Gradually raise fan speed from 60% to 100% as temperature increases from 50 to 80
        speed = 60 + 40 * ((temp - 50) / 30)
        set_fan_speed(min(int(speed), 100))  # Ensure speed does not exceed 100

while True:
    adjust_fan_curve()
    time.sleep(10)  # Check every 10 seconds
