"""Top Google result URLs via the `googlesearch-python` package (no browser needed)."""


def get_top_links(query, num=5):
    from googlesearch import search  # imported lazily so tests don't need network libs

    return list(search(query, num_results=num))


if __name__ == "__main__":
    print(get_top_links("price of Gold in Mumbai"))
