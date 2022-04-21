
from db.run_sql import run_sql
from models.human import *
from models.zombie import *
from models.zombie_type import *
from models.biting import *
import repositories.human_repository as human_repository
import repositories.zombie_repository as zombie_repository

def save(biting):
    sql = "INSERT INTO bitings (human_id, zombie_id) VALUES (%s, %s) RETURNING id"
    values = [biting.human.id, biting.zombie.id]
    results = run_sql(sql, values)
    biting.id = results[0]['id']
    return biting 

def select_all():
    bitings = []

    sql = "SELECT * FROM bitings"
    results = run_sql(sql)

    for row in results:
        human = human_repository.select(row['human_id'])
        zombie = zombie_repository.select(row['zombie_id'])
        biting = Biting(human, zombie, row(['id']))
        bitings.append(biting)
    return bitings 

def select(id):
    # bitings = None

    # sql = "SELECT * FROM bitings WHERE id = %s"
    # values = [id]

    # results = run_sql(sql, values)

    # if len(results) > 0:
    #     result = results[0]
    #     print(results['human_id'])
    # #     bitings = models.Biting(result['human'], result['zombie'], result['id'])
    # # return bitings

    biting = None 
    sql = "SELECT * FROM bitings WHERE id = %s"
    values = [id]

    results = run_sql(sql, values)

    # checking if the list returned by `run_sql(sql, values)` is empty. Empty lists are 'fasly' 
    # Could alternativly have..
    # if len(results) > 0 
    if results:
        result = results[0]
        human = human_repository.select(result["human_id"])
        zombie = zombie_repository.select(result["zombie_id"])
        biting = Biting(human, zombie, result["id"])
    return biting

def delete(id):
    sql = "DELETE FROM bitings WHERE id = %s"
    values = [id]
    run_sql(sql, values)

def delete_all():
    sql = "DELETE * FROM bitings"
    