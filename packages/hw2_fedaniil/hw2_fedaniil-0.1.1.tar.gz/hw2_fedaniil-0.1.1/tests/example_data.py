import os

example_table = [
    ["Character", "Element of Harmony", "Traits", "Role"],
    ["Twilight Sparkle", "Magic", "Intelligent, studious, organized", "Leader, princess, and learner about friendship"],
    ["Applejack", "Honesty", "Hardworking, dependable, straightforward", "Farm pony, runs Sweet Apple Acres"],
    ["Pinkie Pie", "Laughter", "Energetic, cheerful, spontaneous", "Party planner, brings joy and fun"],
    ["Rarity", "Generosity", "Creative, fashionable, dramatic", "Fashion designer, helps friends look their best"],
    ["Rainbow Dash", "Loyalty", "Brave, competitive, confident", "Pegasus, member of the Wonderbolts"],
    ["Fluttershy", "Kindness", "Gentle, shy, nurturing", "Animal caretaker, empathetic friend"],
]
example_table_str = r"""
\begin{table}[h]
    \centering
    \begin{tabular}{|p{0.25\linewidth}|p{0.25\linewidth}|p{0.25\linewidth}|p{0.25\linewidth}|}
        \hline
        Character & Element of Harmony & Traits & Role \\ \hline
        Twilight Sparkle & Magic & Intelligent, studious, organized & Leader, princess, and learner about friendship \\ \hline
        Applejack & Honesty & Hardworking, dependable, straightforward & Farm pony, runs Sweet Apple Acres \\ \hline
        Pinkie Pie & Laughter & Energetic, cheerful, spontaneous & Party planner, brings joy and fun \\ \hline
        Rarity & Generosity & Creative, fashionable, dramatic & Fashion designer, helps friends look their best \\ \hline
        Rainbow Dash & Loyalty & Brave, competitive, confident & Pegasus, member of the Wonderbolts \\ \hline
        Fluttershy & Kindness & Gentle, shy, nurturing & Animal caretaker, empathetic friend \\ \hline
    \end{tabular}
\end{table}""".lstrip()

example_image = os.path.join(os.path.dirname(__file__), "images", "1068070.png")

