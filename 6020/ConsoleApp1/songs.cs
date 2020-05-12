using System;
using System.Collections.Generic;
using System.Text;

namespace ConsoleApp1
{
    class songs
    {

        private string name;
        private string author;
        private int seconds;

        public songs(string name, string author, int seconds)
        {
            this.name = name;
            this.author = author;
            this.seconds = seconds;
        }

        public override string ToString()
        {
            return this.name + " by " + this.author + " length in seconds " + this.seconds;
        }

        public string GetName()
        {
            return this.name;
        }

        public string GetAuthor()
        {
            return this.author;
        }

        public int GetSeconds()
        {
            return this.seconds;
        }
    }
}
