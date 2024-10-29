from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database.config import engine
from app.utilities import isList, SHA224Hash, timestampSeconds
from app.models.award import AwardModelDB


if __name__ == '__main__':
	from app.actions.awards import AwardActions
	import asyncio

	async def get_all():
		print('GET ALL --------------------------------')
		response = await AwardActions.get_all()
		print(response)
		print('')

		response = await AwardActions.get_all(
			'time_created',
			'DESC'
		)
		print(response)
		print('')

		response = await AwardActions.get_all(
			'time_created',
		)
		print(response)
		print('')

		response = await AwardActions.get_all(
			'time_created',
			'ASC'
		)
		print(response)


	async def get_all_where():
		print('GET ALL WHERE --------------------------------')
		# async def get_all_where(model, conditions: tuple, order_by=None, sort='DESC'):
		response = await AwardActions.get_all_where(
			[
				(AwardModelDB.uuid == 'uuid1')
			]
		)
		print(response)
		print('')
		response = await AwardActions.get_all_where(
			[
				(AwardModelDB.time_created > 2)
			]
		)
		print(response)
		print('')


	# asyncio.run(create())
	# asyncio.run(get_all())
	asyncio.run(get_all_where())
