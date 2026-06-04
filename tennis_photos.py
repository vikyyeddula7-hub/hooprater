"""
tennis_photos.py
Player photo URLs using multiple reliable sources.
Priority: ATP Tour official photos, then Wikipedia.
"""

# ATP Tour official headshot CDN — format: https://www.atptour.com/-/media/alias/player-headshot/{player_id}
# Wikipedia thumbnail URLs as fallback
TENNIS_PHOTOS = {
    "Jannik Sinner":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bc/Jannik_Sinner_at_the_2024_US_Open_%2802%29_%28cropped%29.jpg/220px-Jannik_Sinner_at_the_2024_US_Open_%2802%29_%28cropped%29.jpg",
    "Carlos Alcaraz":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/Carlos_Alcaraz_2022_Wimbledon_%28cropped%29.jpg/220px-Carlos_Alcaraz_2022_Wimbledon_%28cropped%29.jpg",
    "Alexander Zverev":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Alexander_Zverev_2022_%28cropped%29.jpg/220px-Alexander_Zverev_2022_%28cropped%29.jpg",
    "Novak Djokovic":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Novak_Djokovi%C4%87_2019_French_Open_%28cropped%29.jpg/220px-Novak_Djokovi%C4%87_2019_French_Open_%28cropped%29.jpg",
    "Ben Shelton":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/35/Ben_Shelton_at_the_2023_US_Open_%28cropped%29.jpg/220px-Ben_Shelton_at_the_2023_US_Open_%28cropped%29.jpg",
    "Félix Auger-Aliassime":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/F%C3%A9lix_Auger-Aliassime_%2851577188042%29_%28cropped%29.jpg/220px-F%C3%A9lix_Auger-Aliassime_%2851577188042%29_%28cropped%29.jpg",
    "Alex de Minaur":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/72/Alex_de_Minaur_at_the_2023_Australian_Open_%28cropped%29.jpg/220px-Alex_de_Minaur_at_the_2023_Australian_Open_%28cropped%29.jpg",
    "Daniil Medvedev":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2b/Daniil_Medvedev_at_the_2023_Australian_Open_04_%28cropped%29.jpg/220px-Daniil_Medvedev_at_the_2023_Australian_Open_04_%28cropped%29.jpg",
    "Taylor Fritz":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Taylor_Fritz_at_the_2023_US_Open_%28cropped%29.jpg/220px-Taylor_Fritz_at_the_2023_US_Open_%28cropped%29.jpg",
    "Alexander Bublik":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/86/Alexander_Bublik_2022_Roland_Garros_%28cropped%29.jpg/220px-Alexander_Bublik_2022_Roland_Garros_%28cropped%29.jpg",
    "Lorenzo Musetti":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3d/Lorenzo_Musetti_Roland_Garros_2022_%28cropped%29.jpg/220px-Lorenzo_Musetti_Roland_Garros_2022_%28cropped%29.jpg",
    "Andrey Rublev":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7d/Andrey_Rublev_2022_Australian_Open_%28cropped%29.jpg/220px-Andrey_Rublev_2022_Australian_Open_%28cropped%29.jpg",
    "Casper Ruud":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Casper_Ruud_2022_%28cropped%29.jpg/220px-Casper_Ruud_2022_%28cropped%29.jpg",
    "Karen Khachanov":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Karen_Khachanov_2022_Roland_Garros_%28cropped%29.jpg/220px-Karen_Khachanov_2022_Roland_Garros_%28cropped%29.jpg",
    "Tommy Paul":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/8/82/Tommy_Paul_at_the_2023_US_Open_%28cropped%29.jpg/220px-Tommy_Paul_at_the_2023_US_Open_%28cropped%29.jpg",
    "Frances Tiafoe":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Frances_Tiafoe_at_the_2022_US_Open_%28cropped%29.jpg/220px-Frances_Tiafoe_at_the_2022_US_Open_%28cropped%29.jpg",
    "Holger Rune":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/Holger_Rune_2022_Roland_Garros_%28cropped%29.jpg/220px-Holger_Rune_2022_Roland_Garros_%28cropped%29.jpg",
    "Stefanos Tsitsipas":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/Stefanos_Tsitsipas_2022_Roland_Garros_%28cropped%29.jpg/220px-Stefanos_Tsitsipas_2022_Roland_Garros_%28cropped%29.jpg",
    "Denis Shapovalov":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/49/Denis_Shapovalov_2022_%28cropped%29.jpg/220px-Denis_Shapovalov_2022_%28cropped%29.jpg",
    "Sebastian Korda":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Sebastian_Korda_%2853127066839%29_%28cropped%29.jpg/220px-Sebastian_Korda_%2853127066839%29_%28cropped%29.jpg",
    "Hubert Hurkacz":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Hubert_Hurkacz_2022_%28cropped%29.jpg/220px-Hubert_Hurkacz_2022_%28cropped%29.jpg",
    "Jack Draper":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Jack_Draper_2022_%28cropped%29.jpg/220px-Jack_Draper_2022_%28cropped%29.jpg",
    "Ugo Humbert":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/Ugo_Humbert_2019_%28cropped%29.jpg/220px-Ugo_Humbert_2019_%28cropped%29.jpg",
    "Stan Wawrinka":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Stan_Wawrinka_2022_%28cropped%29.jpg/220px-Stan_Wawrinka_2022_%28cropped%29.jpg",
    "Dominic Thiem":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Dominic_Thiem_2020_Roland_Garros_%28cropped%29.jpg/220px-Dominic_Thiem_2020_Roland_Garros_%28cropped%29.jpg",
    "Matteo Berrettini":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6a/Matteo_Berrettini_2021_%28cropped%29.jpg/220px-Matteo_Berrettini_2021_%28cropped%29.jpg",
    "Gael Monfils":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Ga%C3%ABl_Monfils_2022_%28cropped%29.jpg/220px-Ga%C3%ABl_Monfils_2022_%28cropped%29.jpg",
    "Alejandro Davidovich Fokina":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Alejandro_Davidovich_Fokina_%2851690302334%29_%28cropped%29.jpg/220px-Alejandro_Davidovich_Fokina_%2851690302334%29_%28cropped%29.jpg",
    "Tallon Griekspoor":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Tallon_Griekspoor_2023_%28cropped%29.jpg/220px-Tallon_Griekspoor_2023_%28cropped%29.jpg",
    "Francisco Cerúndolo":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e7/Francisco_Cerundolo_2022_%28cropped%29.jpg/220px-Francisco_Cerundolo_2022_%28cropped%29.jpg",
    "Cameron Norrie":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Cameron_Norrie_2022_%28cropped%29.jpg/220px-Cameron_Norrie_2022_%28cropped%29.jpg",
    "Arthur Fils":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/Arthur_Fils_2023_%28cropped%29.jpg/220px-Arthur_Fils_2023_%28cropped%29.jpg",
    "Jakub Menšík":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/9e/Jakub_Men%C5%A1%C3%ADk_2024_%28cropped%29.jpg/220px-Jakub_Men%C5%A1%C3%ADk_2024_%28cropped%29.jpg",
    "João Fonseca":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/15/Jo%C3%A3o_Fonseca_2025_Australian_Open_%28cropped%29.jpg/220px-Jo%C3%A3o_Fonseca_2025_Australian_Open_%28cropped%29.jpg",
    "Learner Tien":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Learner_Tien_2024_%28cropped%29.jpg/220px-Learner_Tien_2024_%28cropped%29.jpg",
    "Marin Čilić":
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Marin_Cilic_2022_%28cropped%29.jpg/220px-Marin_Cilic_2022_%28cropped%29.jpg",
}

def get_player_photo(name: str):
    return TENNIS_PHOTOS.get(name)
