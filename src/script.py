from core import compute_rer_route, compute_metro_route, format_result

# df = compute_rer_route(initial_station="La Défense", line="rer_a", direction="right_destination")
df = compute_metro_route(destination="École Vétérinaire de Maisons-Alfort TO Balard", line="metro_8")

print(df.head())
print(format_result(df))

