import csv
import random
import datetime

def generate_synthetic_data(filename):
    nodes = [f"User_{i}" for i in range(1, 51)]
    nodes.insert(0, "Me") # The root user
    
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Source", "Target", "Frequency", "Recency_Days_Ago", "Context"])
        
        # Connect 'Me' to some direct connections (1-hop)
        for i in range(1, 15):
            writer.writerow(["Me", nodes[i], random.randint(1, 50), random.randint(1, 100), "Email"])
            
        # Create 2-hop and 3-hop connections
        for _ in range(100):
            source = random.choice(nodes)
            target = random.choice(nodes)
            if source != target:
                freq = random.randint(1, 20)
                recency = random.randint(1, 365)
                context = random.choice(["Email", "Calendar", "LinkedIn"])
                writer.writerow([source, target, freq, recency, context])

if __name__ == "__main__":
    generate_synthetic_data("data/Connections.csv")
    print("Synthetic data generated.")
