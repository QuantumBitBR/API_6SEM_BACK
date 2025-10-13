from config.db_connection import get_cursor
from utils.encryptor import decrypt_data
from datetime import datetime
from typing import Optional, List, Tuple, Any, Union, Dict

class TicketsRepository:

    def _build_where_clause_and_params(
        self,
        company_id: Optional[List[int]] = None, 
        product_id: Optional[List[int]] = None, 
        category_id: Optional[List[int]] = None, 
        priority_id: Optional[List[int]] = None, 
        createdat: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Tuple[str, List[Any]]:
        """
        Constrói a cláusula WHERE e a lista de parâmetros para a consulta SQL.
        Ajustado para usar 'IN' para listas de IDs.
        """
        conditions = []
        params = []
        
        # Mapeamento para simplificar a lógica de 'IN'
        id_filters = {
            'companyid': company_id,
            'productid': product_id,
            'categoryid': category_id,
            'priorityid': priority_id,
        }
        
        for col_suffix, ids in id_filters.items():
            if ids is not None and ids:
                conditions.append(f"t.{col_suffix} IN %s")
                params.append(tuple(ids))
                
        if createdat is not None:
            conditions.append("t.createdat >= %s")
            params.append(createdat)
            
        if end_date is not None:
            conditions.append("t.createdat <= %s")
            params.append(end_date)

        sql_where = " WHERE " + " AND ".join(conditions) if conditions else ""
        
        return sql_where, params
    

    def get_tickets_by_company(
        self,
        company_id: Optional[int] = None,
        product_id: Optional[int] = None,
        category_id: Optional[int] = None,
        priority_id: Optional[int] = None,
        createdat: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Any]:
        """
        Executa a consulta no banco de dados para contar os tickets por empresa,
        aplicando filtros opcionais.
        """
        sql_base = """
            SELECT 
                c.name,
                COUNT(t.ticketid) AS ticket_count
            FROM 
                tickets t
            JOIN 
                companies c ON t.companyid = c.companyid
            JOIN
                products p ON t.productid = p.productid
            JOIN
                categories ca ON t.categoryid = ca.categoryid
            JOIN
                priorities prio ON t.priorityid = prio.priorityid
        """
        sql_group_by = " GROUP BY c.name;"

        sql_where, params = self._build_where_clause_and_params(
            company_id=company_id,
            product_id=product_id,
            category_id=category_id,
            priority_id=priority_id,
            createdat=createdat,
            end_date=end_date
        )
        
        sql_query = sql_base + sql_where + sql_group_by
        
        with get_cursor() as cur:
            cur.execute(sql_query, tuple(params))
            return cur.fetchall()
        
    def get_tickets_by_product(self):
        """
        Executa a consulta no banco de dados para contar os tickets por produto.
        """
        sql_query = """
            SELECT
                p.name,
                COUNT(t.ticketid) AS ticket_count
            FROM
                tickets t
            JOIN
                products p ON t.productid = p.productid
            GROUP BY
                p.name;
        """

        with get_cursor() as cur:
            cur.execute(sql_query)
            return cur.fetchall()

    def get_tickets_by_category(self):
        """
        Executa a consulta no banco de dados para contar os tickets por categoria.
        """
        sql_query = """
            SELECT
                ca.name,
                COUNT(t.ticketid) AS ticket_count
            FROM
                tickets t
            JOIN
                categories ca ON t.categoryid = ca.categoryid
            GROUP BY
                ca.name;
        """

        with get_cursor() as cur:
            cur.execute(sql_query)
            return cur.fetchall()

    def get_tickets_by_status(self):
        """
        Executa a consulta no banco de dados para contar os tickets por status.
        """
        sql_query = """
            WITH total_tickets AS (
                SELECT COUNT(DISTINCT ticketid) AS total_count
                FROM ticketstatushistory
            )
            SELECT
                s.name,
                CAST(COUNT(s.name) AS REAL) * 100 / (SELECT total_count FROM total_tickets) AS percentage
            FROM
                ticketstatushistory tsh
            JOIN
                statuses s ON tsh.tostatusid = s.statusid
            WHERE
                tsh.historyid IN (
                    SELECT MAX(historyid)
                    FROM ticketstatushistory
                    GROUP BY ticketid
                )
            GROUP BY
                s.name;
        """
        
        with get_cursor() as cur:
            cur.execute(sql_query)
            return cur.fetchall()
        
    def get_by_id(self, id: int):
        sql_query = """
            SELECT 
                t.ticketid,
                t.description, 
                t.title, 
                c.name AS company_name, 
                p.name AS product_name, 
                cat.name AS category_name, 
                s2.name AS subcategory_name,
                prio.name AS priority_name, 
                s.name AS status_name, 
                t.channel, 
                t.device, 
                e.keyencrypt
            FROM tickets t
            INNER JOIN companies c ON c.companyid = t.companyid
            INNER JOIN priorities prio ON prio.priorityid = t.priorityid
            INNER JOIN products p ON p.productid = t.productid
            INNER JOIN statuses s ON s.statusid = t.currentstatusid 
            INNER JOIN categories cat ON cat.categoryid = t.categoryid
            INNER JOIN subcategories s2 ON s2.subcategoryid = t.subcategoryid 
            INNER JOIN encrypt_ticket e ON e.ticketid = t.ticketid
            WHERE t.ticketid = %s;
        """

        with get_cursor() as cur:
            cur.execute(sql_query, (int(id),))
            row = cur.fetchone()
            if not row:
                raise ValueError(f"Id {id} não encontrado!")

            if isinstance(row, tuple):
                colnames = [desc[0] for desc in cur.description]
                row = dict(zip(colnames, row))

            for k, v in row.items():
                if isinstance(v, memoryview):
                    row[k] = v.tobytes().decode('utf-8')

            key = row['keyencrypt']
            row['title'] = decrypt_data(key, row['title'])
            row['description'] = decrypt_data(key, row['description'])

            row.pop('keyencrypt', None)

            return row
                
    def get_by_priority(self):
        """
        Executa a consulta no banco de dados para contar os tickets por prioridade.
        """
        sql_query = """
            select p.name, count(p.name) as total  from tickets t
            inner join priorities p
            on t.priorityid = p.priorityid
            group by p.name;
        """

        with get_cursor() as cur:
            cur.execute(sql_query)
            return cur.fetchall()
        
    def get_tickets_by_department(self):
        """
        Executa a consulta no banco de dados para contar os tickets por departamento,
        fazendo JOINs indiretos: tickets -> agents -> departments.
        Retorna uma lista de tuplas.
        """
        sql_query = """
            SELECT
                d.name,
                COUNT(t.ticketid) AS ticket_count
            FROM
                tickets t
            JOIN
                agents a ON t.assignedagentid = a.agentid
            JOIN
                departments d ON a.departmentid = d.departmentid
            GROUP BY
                d.name;
        """
        
        with get_cursor() as cur:
            cur.execute(sql_query)
            return cur.fetchall()
        

    def get_tickets_by_slaplan(self):
        # mudar para que a porcentagem so retorne dois numeros depois da virgula
        """
        Executa a consulta no banco de dados para contar os tickets por SLAPlan.
        Retorna uma lista de tuplas (slaplan_name, ticket_count).
        """
        sql_query = """
            WITH total_tickets AS (
                SELECT COUNT(ticketid) AS total_count
                FROM tickets
                WHERE slaplanid IS NOT NULL
            )
            SELECT
                sp.name,
                CAST(
                    ROUND(
                        CAST(COUNT(sp.name) AS NUMERIC) * 100 / (SELECT total_count FROM total_tickets),
                        2
                    ) AS DOUBLE PRECISION
                ) AS percentage
            FROM
                tickets t
            JOIN
                sla_plans sp ON t.slaplanid = sp.slaplanid
            GROUP BY
                sp.name;
        """
        with get_cursor() as cur:
            cur.execute(sql_query)
            return cur.fetchall()
