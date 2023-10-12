using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Sadovodstvo
{
    public class Postroyki
    {
        public virtual int id { get; set; }
        public virtual int id_участка { get; set; }
        public virtual string тип_постройки { get; set; }
        public virtual string стоимость_постройки { get; set; }
    }
}
