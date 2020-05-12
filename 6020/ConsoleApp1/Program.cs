using System;

namespace ConsoleApp1
{
    class Program
    {
        static void Main(string[] args)
        {

            int[] numbers = new int[10];
            int[] numbers2 = new int[30];
            numbers[0] = 7;
            
            songs s1 = new songs("creep", "radiohead", 180);
            songs s2 = new songs("hotel california", "the eagles", 200);

            songs[] mixtape = new songs[4];
            songs[] greatesthits = new songs[10];

            mixtape[0] = new songs("hey jude", "the beatles", 420);
            mixtape[1] = new songs("your song", "elton john", 180);

            PrintAlbum(mixtape);

            Console.WriteLine("songs in album = {0}", AlbumSize(mixtape));

            Console.WriteLine("songs int album = {0}", AlbumSize(greatesthits));
              

            Console.ReadLine();
        }

        static int AlbumSize(songs[] album)
        {

            int count = 0;
          
            for (int i = 0; i < album.Length; i++)
            {
                if (album[i] != null)
                    count++;

            }

            return count;
        }
        
        static void PrintAlbum(songs[] album)
        {

            for (int i = 0; i < album.Length; i++)
            {
               if (album[i] != null)
                    Console.WriteLine(album[i].ToString());
             
            }
        }


        static void AddSongToAlbum (songs s, songs[] album)
        {

            for (int i = 0; i < album.Length; i++)
            {

                if(album[i] == null)
                {
                    album[i] = s;
                    return;
                }
            }

            Console.WriteLine("sorry can't add song, the album is full");
        }
    }
}
