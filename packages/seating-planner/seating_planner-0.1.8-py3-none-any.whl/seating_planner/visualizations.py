"""Visualization utilities for SeatingPlanner."""

import altair as alt
import pandas as pd

def plot_overall_satisfaction(results, guest_groups):
    """
    Create a stacked bar chart showing the satisfaction levels of 
    guest seating arrangements using Altair.

    Args:
        results (dict): Results dictionary from SeatingPlanner
        preferences (list): List of preference tuples
        conflicts (list): List of conflict tuples
        guest_groups (dict): Dictionary of guest groups and their sizes
    """
    # Calculate satisfaction metrics
    total_guests = sum(guest_groups.values())
    violated_preferences = {g: guest_groups[g] for v in results['violations']['preferences']
                          for g in v['guests']}
    violated_conflicts = {g: guest_groups[g] for v in results['violations']['conflicts']
                        for g in v['guests']}

    # Calculate categories with actual guest counts
    categories = {
        'Fully Satisfied': sum(
            size for guest, size in guest_groups.items()
            if guest not in violated_preferences and guest not in violated_conflicts
        ),
        'Preference Violated': sum(
            guest_groups[guest] for guest in violated_preferences.keys()
            if guest not in violated_conflicts
        ),
        'Conflict Violated': sum(
            guest_groups[guest] for guest in violated_conflicts.keys()
            if guest not in violated_preferences
        ),
        'Both Violated': sum(
            guest_groups[guest]
            for guest in set(violated_preferences.keys()) & set(violated_conflicts.keys())
        )
    }

    # Create DataFrame for Altair
    df = pd.DataFrame([
        {
            'category': cat,
            'guests': count,
            'percentage': (count/total_guests * 100),
            'label': f"{cat}\n({count} guests, {(count/total_guests * 100):.1f}%)",
            'order': order
        }
        for order, (cat, count) in enumerate([
            ('Fully Satisfied', categories['Fully Satisfied']),
            ('Preference Violated', categories['Preference Violated']),
            ('Conflict Violated', categories['Conflict Violated']),
            ('Both Violated', categories['Both Violated'])
        ])
    ])

    # Create the stacked bar chart
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X('sum(guests):Q',
                axis=alt.Axis(title='Number of Guests'),
                scale=alt.Scale(domain=[0, total_guests])),
        y=alt.Y('category:N',
                axis=None,
                sort=['Fully Satisfied', 'Preference Violated',
                      'Conflict Violated', 'Both Violated']),
        color=alt.Color('category:N',
                       scale=alt.Scale(
                           domain=['Fully Satisfied', 'Preference Violated',
                                 'Conflict Violated', 'Both Violated'],
                           range=['#2ecc71', '#f1c40f', '#e74c3c', '#c0392b']
                       ),
                       legend=alt.Legend(
                           orient='bottom',
                           title=None,
                           labelLimit=200
                       )),
        order=alt.Order('order:Q'),
        tooltip=[
            alt.Tooltip('category:N', title='Category'),
            alt.Tooltip('guests:Q', title='Guests', format='d'),
            alt.Tooltip('percentage:Q', title='Percentage', format='.1f')
        ]
    ).properties(
        width=600,
        height=60,  # Control bar height
        title=alt.TitleParams(
            f'Guest Satisfaction Distribution (Total Guests: {total_guests})',
            fontSize=16,
            anchor='middle'
        )
    )

    # Add text labels on the bars
    text = alt.Chart(df).mark_text(
        align='left',
        baseline='middle',
        dx=5,  # Offset from the end of the bar
        fontSize=12,
        color='white'
    ).encode(
        x=alt.X('sum(guests):Q'),
        y=alt.Y('category:N',
                sort=['Fully Satisfied', 'Preference Violated',
                      'Conflict Violated', 'Both Violated']),
        text=alt.Text('label:N'),
        order=alt.Order('order:Q')
    )

    # Combine chart and text
    final_chart = (chart + text).configure_view(
        strokeWidth=0
    ).configure_axis(
        grid=False
    ).configure_legend(
        labelFontSize=12,
        padding=10,
        columnPadding=10
    )

    return final_chart
