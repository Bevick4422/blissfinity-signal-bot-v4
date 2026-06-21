from performance import get_stats


def build_weekly_report():

    stats = get_stats()

    if stats is None:

        return (
            "📊 WEEKLY REPORT\n\n"
            "No completed trades yet."
        )

    return f"""
📊 BLISSFINITY WEEKLY REPORT

Trades: {stats['total']}

Wins: {stats['wins']}
Losses: {stats['losses']}

Win Rate:
{stats['winrate']}%

Total RR:
{stats['total_rr']}R

Average RR:
{stats['avg_rr']}R
"""