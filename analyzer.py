import random

TECHNIQUES = [
    "Armbar", "Triangle", "Omoplata", "Guillotine", "Rear Naked Choke",
    "Kimura", "Americana", "Ezekiel", "Peruvian Necktie", "Heel Hook",
    "Straight Ankle Lock", "Calf Slicer", "Banana Split", "Toe Hold",
    "X-Guard Sweep", "Lumberjack Sweep", "Scissor Sweep", "Hip Bump",
    "Double Leg", "Single Leg", "Inside Trip", "Outside Trip",
    "Pull Guard", "Sit Up Guard", "Toreando Pass", "Over Under Pass",
    "Knee Cut Pass", "Leg Drag", "Body Lock Pass", "Half Guard Recovery",
    "Shoulder Crunch Sweep", "Electric Chair", "Deep Half Sweep",
    "Berimbolo", "Matrix Back Take", "Crab Ride", "Twister Hook",
    "Deep De La Riva Sweep", "Rolling Back Take", "Kiss of the Dragon",
    "Stack Pass", "North-South Escape", "Bridge & Roll", "Technical Mount",
    "Leg Pin Pass", "Tripod Sweep", "Double Sleeve Sweep", "Loop Choke",
    "Paper Cutter", "North-South Choke", "Wrist Lock", "Bulldog Choke",
    "Flying Armbar", "Flying Triangle", "Standing Guillotine", "Rolling Kimura",
    "Inverted Triangle", "No Arm Triangle", "Submission Chain", "Mount Retention",
    "Back Retention", "Side Control Escape", "Kesa Gatame Escape",
    "Butterfly Sweep", "Reverse De La Riva Sweep", "Saddle Entry",
    "Ashigarami Setup", "False Reap Entry", "Leg Entanglement",
    "Wrestle-Up Sweep", "Lapel Guard Setup", "Worm Guard Sweep",
    "Baratoplata", "Shoulder Pin", "Can Opener Pass", "Stack Escape",
    "Sit Through Escape", "Elbow Push Escape", "Leg Trap Pass"
]

def run_fake_analysis(filename):
    detected = random.sample(TECHNIQUES, k=6)
    return {
        "filename": filename,
        "detected_techniques": detected,
        "summary": f"{len(detected)} techniques recognized. Solid round!"
    }
