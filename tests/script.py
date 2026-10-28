from src.api.domain.core import format_result
from src.api.domain.rer import compute_rer_route
from src.api.domain.metro import compute_metro_route

# df = compute_rer_route(initial_station="La Défense", line="rer_a", direction="right_destination")
df = compute_metro_route(destination="École Vétérinaire de Maisons-Alfort TO Balard", line="metro_8")

print(df.head())
print(format_result(df))

