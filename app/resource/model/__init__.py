from app.db.db import Base

# ここにモデルを読ませないと、alembicでmigrationファイルが生成されない
from app.resource.model.users import User