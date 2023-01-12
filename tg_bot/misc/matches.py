import math

from tg_bot.types.stage import Stage
from tg_bot.types.match.status import MatchStatus


async def grouping(db_model):
    tournament_teams = await db_model.get_tournament_teams()

    limit_group = 8

    groups = ['A', 'B', 'C', 'D']

    for index in range(len(tournament_teams)):
        group = groups[math.ceil((index + 1) / limit_group) - 1]
        tournament_team = tournament_teams[index]
        await db_model.set_tournament_team_group(tournament_team_id=tournament_team.id, group=group)


async def add_matches(db_model):
    await db_model.add_match(number_match=1, next_number_match=9, stage=Stage.QUARTERFINAL, group='A', match_status=MatchStatus.TEAM_COMPLETE, first_tournament_team_id=1, second_tournament_team_id=2)
    await db_model.add_match(number_match=2, next_number_match=9, stage=Stage.QUARTERFINAL, group='A', match_status=MatchStatus.TEAM_COMPLETE, first_tournament_team_id=3, second_tournament_team_id=4)
    await db_model.add_match(number_match=3, next_number_match=10, stage=Stage.QUARTERFINAL, group='A', match_status=MatchStatus.TEAM_COMPLETE, first_tournament_team_id=5, second_tournament_team_id=6)
    await db_model.add_match(number_match=4, next_number_match=10, stage=Stage.QUARTERFINAL, group='A', match_status=MatchStatus.TEAM_COMPLETE, first_tournament_team_id=7, second_tournament_team_id=8)
    await db_model.add_match(number_match=5, next_number_match=11, stage=Stage.QUARTERFINAL, group='B', match_status=MatchStatus.TEAM_COMPLETE, first_tournament_team_id=9, second_tournament_team_id=10)
    await db_model.add_match(number_match=6, next_number_match=11, stage=Stage.QUARTERFINAL, group='B', match_status=MatchStatus.TEAM_COMPLETE, first_tournament_team_id=11, second_tournament_team_id=12)
    await db_model.add_match(number_match=7, next_number_match=12, stage=Stage.QUARTERFINAL, group='B', match_status=MatchStatus.TEAM_COMPLETE, first_tournament_team_id=13, second_tournament_team_id=14)
    await db_model.add_match(number_match=8, next_number_match=12, stage=Stage.QUARTERFINAL, group='B', match_status=MatchStatus.TEAM_COMPLETE, first_tournament_team_id=15, second_tournament_team_id=16)

    await db_model.add_match(number_match=9, next_number_match=13, stage=Stage.SEMIFINAL, group='A')
    await db_model.add_match(number_match=10, next_number_match=13, stage=Stage.SEMIFINAL, group='A')
    await db_model.add_match(number_match=11, next_number_match=13, stage=Stage.SEMIFINAL, group='B')
    await db_model.add_match(number_match=12, next_number_match=13, stage=Stage.SEMIFINAL, group='B')

    await db_model.add_match(number_match=13, stage=Stage.FINAL)
    await db_model.add_match(number_match=14, stage='THIRD PLACE')


# async def add_opening_matches(db_model):
#     limit_group = 8
#
#     tournament_teams = await db_model.get_tournament_teams()
#
#     print(f'Кол-во команд: {len(tournament_teams)}')
#
#     count_groups = len(tournament_teams) // limit_group
#     groups = ['A', 'B', 'C', 'D']
#
#     for group in range(count_groups):
#         tournament_teams_for_group = await db_model.get_tournament_teams_by_group(group=groups[group])
#         print(f'Кол-во команда в группе {groups[group]}: {len(tournament_teams_for_group)}')
#
#         for index in range(0, limit_group, 2):
#             print(f'Текущий индекс: {index}')
#
#             first_tournament_team = tournament_teams_for_group[index].id
#             second_tournament_team = tournament_teams_for_group[index + 1].id
#
#             print(f'ID первой команды:{first_tournament_team}')
#             print(f'ID второй команды:{second_tournament_team}')
#
#             await db_model.add_match(
#                 first_tournament_team_id=first_tournament_team,
#                 second_tournament_team_id=second_tournament_team,
#                 stage=Stage.QUARTERFINAL,
#                 group=groups[group]
#             )
