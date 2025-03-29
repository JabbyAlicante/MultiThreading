# 🎮 Characters Queueing Simulator
This project simulates a party setup based on the game Genshin Impact using Python multithreading. It demonstrates how to manage concurrent data updates with threading locks and semaphores while handling JSON data to simulate real-time party configuration and elemental resonance effects.
## 🌟 Features
✅ Simulates up to 1000 party setups with 4 players

✅ Handles data consistency using Locks and Semaphores

✅ Displays active party members, elemental resonance, and active buffs

✅ Random character selection and update handling
## 🚀 How It Works
1. Each player selects a character randomly from a pool.

2. The system updates the party setup concurrently using threading.

3. Elemental resonance and buffs are calculated based on character elements.

4. Results are saved to a JSON file (new_party_setup.json).

5. The simulation ensures data consistency with threading locks and semaphores.
## 🧠 Writers-Readers Problem
This project demonstrates a writers-readers problem:

📖 Multiple threads (players) can read the data concurrently.

✍️ Writing (updating party data) requires exclusive access to avoid race conditions.

🔒 A Lock prevents reading and writing from interfering with each other.

🚦 A Semaphore limits the number of concurrent writers to avoid data corruption.

This ensures that reading and writing operations remain consistent even when multiple threads are running.

## 🛠️ **Technologies Used**  

| 🏷️ Technology             | 🚀 Description                                   |  
|--------------------------|--------------------------------------------------|  
| 🐍 **Python**             | Core programming language used for simulation    |  
| 🧵 **Threading**          | For handling concurrent data updates             |  
| 🔒 **Lock and Semaphore** | To prevent race conditions and control write access |  
| 📄 **JSON**               | For data storage and processing                  |  

## 📥 Setup  

1. Clone the repository:  
```bash git clone https://github.com/JabbyAlicante/MultiThreading.git```
2. Navigate to the project directory:
```cd MultiThreading then cd charactersQueue```
3. Install dependencies :
```pip install -r requirements.txt```
4. Then run the simulation.

## 🎯 How to Customize
➕ Add new characters and elements to the character_elements dictionary.

🔧 Modify buff conditions or effects in the party_buffs dictionary.

## 🤝 Contributing
Feel free to submit pull requests or open issues for improvements or bug fixes.
