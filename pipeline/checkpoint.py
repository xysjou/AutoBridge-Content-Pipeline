from datetime import datetime,timezone
def save(db,batch_id,cursor):
 db.execute('INSERT INTO checkpoints(batch_id,cursor,updated_at) VALUES(?,?,?) ON CONFLICT(batch_id) DO UPDATE SET cursor=excluded.cursor,updated_at=excluded.updated_at',(batch_id,cursor,datetime.now(timezone.utc).isoformat())); db.commit()
def load(db,batch_id):
 row=db.execute('SELECT cursor FROM checkpoints WHERE batch_id=?',(batch_id,)).fetchone(); return row[0] if row else 0
