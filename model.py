import random
import math

class Set:
    def __init__(self, set_type, dist):
        self.set_type = set_type
        self.dist = dist 
        self.num_rounds = 1
        self.sets = []
        if set_type.lower() == "warmup":
            self.warmup(dist)
        if set_type.lower() == "cooldown":
            self.cooldown(dist)
        if set_type.lower() == "main set":
            self.main_set(dist)
        self.set_dist = self.get_set_dist(self.sets) * self.num_rounds

    def get_swim_dist(self, swim):
        return swim[0]*swim[1]

    def get_set_dist(self, sets):
        dist = 0
        for swim in self.sets:
            dist += self.get_swim_dist(swim)
        return dist

    def divide_evenly(self, dist, rounds):
        return (dist / rounds) - (dist / rounds % 25)

    def create_set(self, yards):
        dist = 0
        while dist == 0:
            # half the time pick a random dist, half the time pick from the common distances
            if random.random() > 0.5:
                # this transformation makes it more likely to choose a shorter
                # distance rather than a longer one for each item in a set
                dist = math.floor((random.random()*(math.sqrt(yards)))**2)
                # round down to the nearest 25 yards because that's a pool length
                dist = dist - (dist % 25)
            else:
                dist = random.choice([50, 75, 100, 150])

            # if dist is above the max, set it equal to the max
            if dist <= 25:
                dist = 25
            # calculate how many reps can you do, and then choose a random # <= that
            max_reps = math.floor(yards / dist)
            reps = random.randint(1, max_reps)
            if dist % 50 != 0:
                if dist * 2 > yards:
                    dist = dist + 25
                elif reps == 1:
                    reps = 2
                elif reps % 2 != 0:
                    reps -= 1
            return [reps, dist]

    def warmup(self, total_yds):
        sets = []
        if total_yds <= 500: # this set if warmup <500 
            sets.append([1, total_yds-100])
            sets.append([1, 100])
        elif total_yds <= 800: # this set if warmup btwn 500 and 800
            sets.append([1, total_yds-300])
            sets.append([2, 100])
            sets.append([4, 25])
        else: # this set if warm up >800
            sets.append([1, total_yds-500])
            sets.append([4, 75])
            sets.append([4, 50])
        # assign strokes/types to each swim
        for i in range(len(sets)):
            if i == 0:
                sets[i].append("Easy")
            elif i == 1:
                options = ["Drill", "Kick"]
                sets[i].append(random.choice(options))
            else:
                sets[i].append("Choice Solid")
        self.sets = sets

    def cooldown(self, total_yds):
        self.sets = [[1, total_yds, "Easy"]]

    def main_set(self, total_yds):
        self.num_rounds = random.randint(1, 4) # 1-4 rounds for main set 
        print("Total yards" + str(total_yds))
        print("N rounds " + str(self.num_rounds))
        yds_per_round = self.divide_evenly(total_yds, self.num_rounds)
        yards_left = yds_per_round
        sets = [] # this is where we'll save each swim in the entire set
        # add items into the main set until we have less than 15% of the distance left
        while yards_left > 0.15*yds_per_round:
            print("Yards left " + str(yards_left))
            print("Yards in round " + str(yds_per_round))
            set1 = self.create_set(yards_left)
            set1_dist = self.get_swim_dist(set1)
            sets.append(set1)
            yards_left -= set1_dist
        # add the last item to the set
        if yards_left != 0:
            if yards_left == 25:
                sets.append([2,25])
            else:
                sets.append([1,int(yards_left)])
        # assign a stroke/focus to each swim
        for swim in sets:
            if swim[1] in [25, 50, 75]:
                options = ["Free", "Back", "Breast", "Fly", "Kick", "Solid", "Fast", "Build", "Blast", "Choice"]
                swim.append(random.choice(options))
            elif swim[1] in [125, 150, 175]:
                options = ["Free", "Back", "Kick", "Solid", "Fast", "Build", "Choice"]
                swim.append(random.choice(options))
            elif swim[1] in [100, 200]:
                options = ["Free", "IM", "IM", "IM", "Solid", "Fast", "Build", "Choice", "Smooth", "Negative Split"]
                swim.append(random.choice(options))
            else: 
                options = ["Free", "Free", "Solid", "Solid", "Smooth"]
                swim.append(random.choice(options))
        self.sets = sets


# Create workout function starts here

def create_workout(dist):
    workout = []
    dist_swam = 0

    # Calculate the distances for different parts of the workout: warm up, main sets 1 and 2, and the cool down 
    # Warm up will be 20% of that up to 1000 
    # Main set 1 will be 35% 
    # Main set 2 will be 28%
    # Cool down will be 7% (calc as whatever is left)
    dist_wu = int(dist * 0.2 - (dist * 0.2) % 25)
    dist_ms1 = int( (dist)*0.4 - (dist)*0.4 % 25)
    dist_ms2 = int( (dist)*0.32 - (dist)*0.32 % 25)

    # Warm up
    workout.append(Set("warmup", dist_wu))
    # most recent workout add is the last one
    dist_swam += workout[-1].set_dist

    # Main set 1
    workout.append(Set("main set", dist_ms1))
    dist_swam += workout[-1].set_dist

    # Main set 2
    workout.append(Set("main set", dist_ms2))
    dist_swam += workout[-1].set_dist

    # Cool down
    dist_cd = (dist - dist_swam) - (dist - dist_swam) % 25
    workout.append(Set("cooldown", dist_cd))

    return workout
