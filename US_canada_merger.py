# Population of U.S. states and Canadian provinces/territories (approximate)
us_states = {
    "California": 39538223, "Texas": 29145505, "Florida": 21538187, "New York": 20201249,
    "Pennsylvania": 13002700, "Illinois": 12812508, "Ohio": 11799448, "Georgia": 10711908,
    "North Carolina": 10439388, "Michigan": 10077331, "New Jersey": 9288994, "Virginia": 8631393,
    "Washington": 7705281, "Arizona": 7151502, "Massachusetts": 7029917, "Tennessee": 6910840,
    "Indiana": 6785528, "Missouri": 6154913, "Maryland": 6177224, "Wisconsin": 5893718,
    "Colorado": 5773714, "Minnesota": 5706494, "South Carolina": 5118425, "Alabama": 5024279,
    "Louisiana": 4657757, "Kentucky": 4505836, "Oregon": 4237256, "Oklahoma": 3959353,
    "Connecticut": 3605944, "Utah": 3271616, "Iowa": 3190369, "Nevada": 3104614,
    "Arkansas": 3011524, "Mississippi": 2961279, "Kansas": 2937880, "New Mexico": 2117522,
    "Nebraska": 1961504, "West Virginia": 1793716, "Idaho": 1839106, "Hawaii": 1455271,
    "Maine": 1362359, "New Hampshire": 1377529, "Montana": 1084225, "Rhode Island": 1097379,
    "Delaware": 989948, "South Dakota": 886667, "North Dakota": 779094, "Alaska": 733391,
    "Vermont": 643077, "Wyoming": 576851
}

canadian_provinces = {
    "Ontario": 15600000,
    "Quebec": 8800000,
    "British Columbia": 5500000,
    "Alberta": 4700000,
    "Manitoba": 1400000,
    "Saskatchewan": 1200000,
    "Nova Scotia": 1000000,
    "New Brunswick": 830000,
    "Newfoundland and Labrador": 520000,
    "Prince Edward Island": 170000,
    "Northwest Territories": 45000,
    "Yukon": 44000,
    "Nunavut": 40000
}

# Filter provinces with population over 60,000 (the population required for statehood)
eligible_provinces = {k: v for k, v in canadian_provinces.items() if v >= 60000}
print ("eligible provinces (those with population >60,000:")
print (eligible_provinces)
print("...")

# Total U.S. population and representatives
us_population = sum(us_states.values())
us_representatives = 435

# Total population (U.S. + Canada)
total_population_combined = us_population + sum(eligible_provinces.values())
print("Population of US & Eligible Provinces in Canada")
print("US: ", str(us_population))
print("Canada: ", sum(eligible_provinces.values()))
print("Total: ", total_population_combined)
print("...")
# Population per congressional seat
population_per_seat = total_population_combined / us_representatives
print("Population per seat: ", population_per_seat)
print("...")

# Initialize representatives allocation (one seat minimum)
region_representatives = {region: 1 for region in {**us_states, **eligible_provinces}}
print("Assigning a minimum of one representative per district...")

# Calculate remaining representatives after allocating one per region
remaining_seats = us_representatives - len(region_representatives)
print("Assinging remaining", str(remaining_seats), "seats")

# Calculate populations for proportional allocation
remaining_population = {
    region: ({**us_states, **eligible_provinces}[region] - population_per_seat)
    for region in {**us_states, **eligible_provinces}
}

# Sort regions by population size for proportional allocation
sorted_regions = sorted(
    remaining_population.items(), key=lambda x: x[1], reverse=True
)

# Allocate remaining seats proportionally
for _ in range(remaining_seats):
    highest_region = sorted_regions[0][0]
    region_representatives[highest_region] += 1
    sorted_regions = sorted(
        sorted_regions, key=lambda x: {**us_states, **eligible_provinces}[x[0]] / region_representatives[x[0]], reverse=True
    )

# Recalculate current representatives for U.S. states
current_state_representatives = {state: round(us_states[state] / (us_population / us_representatives)) for state in us_states}

# Adjust current representatives to ensure they sum to 435
while sum(current_state_representatives.values()) != us_representatives:
    if sum(current_state_representatives.values()) < us_representatives:
        state_to_increase = max(
            current_state_representatives,
            key=lambda state: us_states[state] / current_state_representatives[state]
        )
        current_state_representatives[state_to_increase] += 1
    else:
        state_to_decrease = min(
            current_state_representatives,
            key=lambda state: us_states[state] / current_state_representatives[state]
        )
        current_state_representatives[state_to_decrease] -= 1

# Merge current and proposed representatives for U.S. states and Canadian provinces
import pandas as pd
merged_representatives = pd.DataFrame({
    "Region": list(current_state_representatives.keys()) + list(eligible_provinces.keys()),
    "Population": [
        us_states.get(region, eligible_provinces.get(region, 0))
        for region in list(current_state_representatives.keys()) + list(eligible_provinces.keys())
    ],
    "Current Representatives": list(current_state_representatives.values()) + [0] * len(eligible_provinces),
    "Proposed Representatives": [
        region_representatives.get(region, 0) for region in list(current_state_representatives.keys()) + list(eligible_provinces.keys())
    ]
})
merged_representatives["Difference"] = (
    merged_representatives["Proposed Representatives"] - merged_representatives["Current Representatives"]
)
merged_representatives.sort_values(by="Proposed Representatives", ascending=False, inplace=True)

# Display the result
merged_representatives

print("merged_representatives:")
print(merged_representatives)