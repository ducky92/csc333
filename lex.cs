using System;
using System.Text;
using System.IO;

namespace project2
{
    class lex
    {
        static int[] rep;
        static void Main(string[] args)
        {
            string file = (args.Length > 0) ? args[0] : "lex.in";
            var path = Directory.GetCurrentDirectory() + "/" + file;
            string[] input = System.IO.File.ReadAllLines(@path) ;
            string[] words = new string[input.Length];
            long[] count = new long[input.Length];
            for (int i = 0; i < input.Length-1; ++i )
            {
                string[] temp = input[i].Split(' ');
                words[i] = temp[0];
                count[i] = long.Parse(temp[1]);
            }
            int index = 0;

            while (index < words.Length-1)
            {
                long K = count[index]-1; // ?
                char[] sa = words[index].ToCharArray();
                Array.Sort(sa);
                rep = new int[sa.Length];
                string str = "";
                char prev = ' ';
                foreach(char ch in sa)
                {
                    if (ch != prev)
                    {
                        rep[str.Length] = 1;
                        str += ch;
                        prev = ch;
                    }
                    else
                    {
                        rep[str.Length - 1]++;
                    }
                }
                Console.WriteLine(solve(K, str.ToCharArray()));
                index++;
            }
            //Console.ReadKey(); // pauses console window
        }
        static long fac(long i)
        {
            long total = 1;
            for(; i > 1; i--)
            {
                total *= i;
            }
            return total;
        }
        static long perm(int total)
        {
            long x = fac(total);
            foreach (int r in rep)
            {
                x /= fac(r);
            }
            return  x;
        }
        static string solve(long K, char[] let)
        {
            int n = rep.Length, d = let.Length;
            char[] sol = new char[n];
            for (int i = 0; i < n; i++)
            {
                for (int j = 0; j < d; j++)
                {
                    if (rep[j] > 0)
                    {
                        rep[j]--;
                        long dk = perm(n - i - 1);
                        if (dk > K)
                        {
                            sol[i] = let[j];
                            break;
                        }
                        rep[j]++;
                        K -= dk;
                    }
                }
            }
            return new string(sol);
        }
    }
}
