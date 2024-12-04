from pyswip import Prolog

prolog = Prolog()
prolog.consult('laptop.pl')
results=prolog.query("start.")
print(list(results))
    
# def get_recommendation(budget, usage, ram):
#     query = f"get_recommendation({budget}, '{usage}', {ram}, R)"
#     results = list(prolog.query(query))
#     return [result['R'] for result in results]

# # budget = 1200
# # usage = 'general'
# # ram = 8
# # recommendations = get_recommendation(budget, usage, ram)
# # print(recommendations)


# def main():
#     budget = int(input("Enter your budget: "))
#     usage = input("Enter the intended usage (e.g., 'gaming', 'business', 'general'): ")
#     ram = int(input("Enter the minimum RAM (GB): "))
    
#     recommendations = get_recommendation(budget, usage, ram)
    
#     if recommendations:
#         print("Recommended Laptops:")
#         for laptop in recommendations:
#             print(laptop)
#     else:
#         print("No laptops match your criteria.")

# if __name__ == "__main__":
#     main()
