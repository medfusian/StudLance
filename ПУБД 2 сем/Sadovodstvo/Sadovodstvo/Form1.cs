using MySql.Data.MySqlClient;
using System;
using System.Data;
using System.Windows.Forms;

namespace Sadovodstvo
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            LoadData();
        }

        private void LoadData()
        {
            DB db = new DB();

            db.openConnection();
            
            MySqlCommand command1 = new MySqlCommand("SELECT * FROM владельцы", db.getConnection());

            MySqlDataReader reader1 = command1.ExecuteReader();

            DataTable table1 = new DataTable();
            table1.Load(reader1);

            dataGridView3.DataSource = table1;

            reader1.Close();
            db.closeConnection();


            MySqlCommand command2 = new MySqlCommand();
            string commandString = "SELECT * FROM участки;";
            command2.CommandText = commandString;
            command2.Connection = db.getConnection();
            MySqlDataReader reader2;
            try
            {
                db.openConnection();
                reader2 = command2.ExecuteReader();
                this.dataGridView4.Columns.Add("id", "id");
                this.dataGridView4.Columns["id"].Width = 20;
                this.dataGridView4.Columns.Add("номер_участка", "номер_участка");
                this.dataGridView4.Columns["номер_участка"].Width = 100;
                this.dataGridView4.Columns.Add("площадь", "площадь");
                this.dataGridView4.Columns["площадь"].Width = 80;
                this.dataGridView4.Columns.Add("взносы_в_фонд_садоводства", "взносы");
                this.dataGridView4.Columns["взносы_в_фонд_садоводства"].Width = 80;
                while (reader2.Read())
                {
                    dataGridView4.Rows.Add(reader2["id"].ToString(), reader2["номер_участка"].ToString(), 
                        reader2["площадь"].ToString(), reader2["взносы_в_фонд_садоводства"].ToString());
                }
                reader2.Close();
            }
            catch (MySqlException ex)
            {
                Console.WriteLine("Error: \r\n{0}", ex.ToString());
            }
            finally
            {
                command2.Connection.Close();
            }
        }
    }
}
