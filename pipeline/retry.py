from datetime import datetime,timedelta,timezone
def enqueue(db,batch_id,article_id,attempts,error,now=None):
 now=now or datetime.now(timezone.utc); due=now+timedelta(seconds=min(3600,2**max(0,attempts))); db.execute('INSERT INTO retry_queue(batch_id,article_id,attempts,next_retry_at,last_error) VALUES(?,?,?,?,?) ON CONFLICT(batch_id,article_id) DO UPDATE SET attempts=excluded.attempts,next_retry_at=excluded.next_retry_at,last_error=excluded.last_error',(batch_id,article_id,attempts,due.isoformat(),error)); db.commit()
def due(db,now=None):
 return db.execute('SELECT batch_id,article_id,attempts,last_error FROM retry_queue WHERE next_retry_at<=? ORDER BY next_retry_at',((now or datetime.now(timezone.utc)).isoformat(),)).fetchall()
