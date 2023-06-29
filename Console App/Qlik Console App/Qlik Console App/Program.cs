using System;
using System.IO;
using System.Diagnostics;
using System.Data.SqlTypes;

namespace demo1
{
    class Program
    {
        static void Main(string[] args)
        {
            // setting the qlik cli 
            List<string> appList = new List<string>();
            string pythonScriptPath = @"C:\Users\MAQ\OneDrive - MAQ Software\Documents\Akash Rajak\Megha Team Assignment\4 - Migration Automation CIP\work\Qlik Extractor\get_list.py";
            //string pythonScriptPath = @"xmlParserV2.py";
            string functioname = "main";

            string context_name = "Akashtest23";
            string qlik_tenant_url = "https://uytp9tpbd684baf.sg.qlikcloud.com/";
            string api_key = "eyJhbGciOiJFUzM4NCIsImtpZCI6IjRmZmU4ZWU2LTIxNTgtNDY0My1iNGE0LTgzZTgxNjBmYjBjNiIsInR5cCI6IkpXVCJ9.eyJzdWJUeXBlIjoidXNlciIsInRlbmFudElkIjoiTkhwaXphMThhU1VwXzQyaEhOemx4Q1hBdEJkRm5pTlciLCJqdGkiOiI0ZmZlOGVlNi0yMTU4LTQ2NDMtYjRhNC04M2U4MTYwZmIwYzYiLCJhdWQiOiJxbGlrLmFwaSIsImlzcyI6InFsaWsuYXBpL2FwaS1rZXlzIiwic3ViIjoiNjQ3NDY4OTM3M2FjOGNiNTFlMzQxNTU1In0.f8VwBYAcBvxSuuo2hhLG3u2GPCZXkjAtufr8a63ohGIxb9pI7XCKqzOn3DXK5mFGjOh7Znb43iLy41TK1h4RBqdiyTwom8n19lFYbBUq3aSG8JWrEJWZo13wBfDiYyk7";
            //string context_name = "Yogeshtest23";
            //string qlik_tenant_url = "https://71kp7fz0e3rbd5p.sg.qlikcloud.com/";
            //string api_key = "eyJhbGciOiJFUzM4NCIsImtpZCI6IjYwNDk0ZWM2LTgyODktNDA1NC1hZDlhLTk5NmI3MzM2N2ZjYiIsInR5cCI6IkpXVCJ9.eyJzdWJUeXBlIjoidXNlciIsInRlbmFudElkIjoieUw5MXZXcG4tMjVybTh0U280UFo3ZGxmVDBYYWtCMV8iLCJqdGkiOiI2MDQ5NGVjNi04Mjg5LTQwNTQtYWQ5YS05OTZiNzMzNjdmY2IiLCJhdWQiOiJxbGlrLmFwaSIsImlzcyI6InFsaWsuYXBpL2FwaS1rZXlzIiwic3ViIjoiNjQ5MTI0MGY5NTE1MDVmMzJiMTAyMjQ1In0.HSHbrYjyrTYQ75sDIJZRHhyING_9Iu_u7X4L6rt6yrrnX2zGDDieXy4L-_8LthDizvluiotCnRYnrj8ijgVJlTxsqFUmA95PJinycAX_naWlz2MPRFiXkuePNAQng9cB";

            string parameters = String.Format("\"{0}\" | \"{1}\" | \"{2}\" | \"{3}\" | \"{4}\"", pythonScriptPath, functioname, context_name, qlik_tenant_url, api_key);

            ProcessStartInfo startInfo = new ProcessStartInfo
            {
                FileName = "python",
                //Arguments = $"{pythonScriptPath} {functioname} {parameter}",
                Arguments = parameters,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                CreateNoWindow = false
            };

            using (Process process = Process.Start(startInfo))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    Console.WriteLine("Qlik CLI Started");
                    string result = reader.ReadToEnd();
                    Console.WriteLine(result);

                    string[] lines = result.Split('\n');
                    //Console.WriteLine(lines.Length);
                    foreach (string line in lines)
                    {
                        //Console.WriteLine("new");
                        //Console.WriteLine(line);
                        bool app = line.Contains("App Name");
                        if (app)
                        {
                            //Console.WriteLine(line);
                            appList.Add(line);
                        }
                    }
                    //foreach (string app_name in appList)
                    //{
                    //    Console.WriteLine(app_name);
                    //}
                    Console.WriteLine("Qlik CLI Stopped");
                }
            }




            // extracting the metadata for the specific qlik crereport
            string pythonScriptPath1 = @"C:\Users\MAQ\OneDrive - MAQ Software\Documents\Akash Rajak\Megha Team Assignment\4 - Migration Automation CIP\work\Qlik Extractor\Qlik_Extractor.py";
            string functioname1 = "main";
            string app_input = "Test App";
            string parameters1 = String.Format("\"{0}\" | \"{1}\" | \"{2}\"", pythonScriptPath1, functioname1, app_input);

            ProcessStartInfo startInfo1 = new ProcessStartInfo
            {
                FileName = "python",
                //Arguments = $"{pythonScriptPath} {functioname} {parameter}",
                Arguments = parameters1,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                CreateNoWindow = false
            };

            using (Process process = Process.Start(startInfo1))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    Console.WriteLine("Extraction Started");
                    Console.WriteLine("Report Name : " + app_input);

                    string result = reader.ReadToEnd();
                    Console.WriteLine(result);

                    Console.WriteLine("Extraction Stopped");
                }
            }

        }
    }
}