"""initial tables

Revision ID: 1d15657b71c3
Revises: 
Create Date: 2025-04-21 12:12:47.988615

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1d15657b71c3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('consultorios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('piso', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('especialidades',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('examenes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=True),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('medicamentos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.Column('precio', sa.Float(), nullable=True),
    sa.Column('cantidad', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pacientes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('apellido', sa.String(length=100), nullable=False),
    sa.Column('fecha_nacimiento', sa.Date(), nullable=False),
    sa.Column('documento', sa.String(length=50), nullable=False),
    sa.Column('telefono', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('documento')
    )
    op.create_index(op.f('ix_pacientes_id'), 'pacientes', ['id'], unique=False)
    op.create_table('roles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('historial_medico',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('paciente_id', sa.Integer(), nullable=True),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.Column('fecha', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['paciente_id'], ['pacientes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('medicos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nombre', sa.String(length=100), nullable=False),
    sa.Column('apellido', sa.String(length=100), nullable=False),
    sa.Column('especialidad_id', sa.Integer(), nullable=True),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('telefono', sa.String(length=20), nullable=True),
    sa.Column('documento', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['especialidad_id'], ['especialidades.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pagos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('paciente_id', sa.Integer(), nullable=True),
    sa.Column('monto', sa.Float(), nullable=True),
    sa.Column('fecha', sa.DateTime(), nullable=True),
    sa.Column('metodo_pago', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['paciente_id'], ['pacientes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('resultados_examenes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('paciente_id', sa.Integer(), nullable=True),
    sa.Column('examen_id', sa.Integer(), nullable=True),
    sa.Column('resultado', sa.Text(), nullable=True),
    sa.Column('fecha_realizacion', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['examen_id'], ['examenes.id'], ),
    sa.ForeignKeyConstraint(['paciente_id'], ['pacientes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('usuarios',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=False),
    sa.Column('rol_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['rol_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('citas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('fecha', sa.DateTime(), nullable=False),
    sa.Column('paciente_id', sa.Integer(), nullable=True),
    sa.Column('medico_id', sa.Integer(), nullable=True),
    sa.Column('consultorio_id', sa.Integer(), nullable=True),
    sa.Column('motivo', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['consultorio_id'], ['consultorios.id'], ),
    sa.ForeignKeyConstraint(['medico_id'], ['medicos.id'], ),
    sa.ForeignKeyConstraint(['paciente_id'], ['pacientes.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('facturas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('pago_id', sa.Integer(), nullable=True),
    sa.Column('detalle', sa.Text(), nullable=True),
    sa.Column('fecha_emision', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['pago_id'], ['pagos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('horarios_medicos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('medico_id', sa.Integer(), nullable=True),
    sa.Column('dia_semana', sa.String(length=20), nullable=True),
    sa.Column('hora_inicio', sa.Time(), nullable=True),
    sa.Column('hora_fin', sa.Time(), nullable=True),
    sa.ForeignKeyConstraint(['medico_id'], ['medicos.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('diagnosticos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cita_id', sa.Integer(), nullable=True),
    sa.Column('descripcion', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['cita_id'], ['citas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('recetas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('cita_id', sa.Integer(), nullable=True),
    sa.Column('instrucciones', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['cita_id'], ['citas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('medicamento_recetado',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('receta_id', sa.Integer(), nullable=True),
    sa.Column('medicamento_id', sa.Integer(), nullable=True),
    sa.Column('dosis', sa.String(length=100), nullable=True),
    sa.ForeignKeyConstraint(['medicamento_id'], ['medicamentos.id'], ),
    sa.ForeignKeyConstraint(['receta_id'], ['recetas.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('medicamento_recetado')
    op.drop_table('recetas')
    op.drop_table('diagnosticos')
    op.drop_table('horarios_medicos')
    op.drop_table('facturas')
    op.drop_table('citas')
    op.drop_table('usuarios')
    op.drop_table('resultados_examenes')
    op.drop_table('pagos')
    op.drop_table('medicos')
    op.drop_table('historial_medico')
    op.drop_table('roles')
    op.drop_index(op.f('ix_pacientes_id'), table_name='pacientes')
    op.drop_table('pacientes')
    op.drop_table('medicamentos')
    op.drop_table('examenes')
    op.drop_table('especialidades')
    op.drop_table('consultorios')
    # ### end Alembic commands ###
