import java.sql.*;
import java.io.*;
import java.util.*;
public class textToDB {

    public static void main(String[] args) {
        try{
            Class test = Class.forName("org.sqlite.JDBC");
        } catch(Exception e){
            System.out.println("run this by adding the classpath to jdbc as if you are getting this error then you did not");
        }
        final String DB_URL = "jdbc:sqlite:log.db";
        // Open a connection
        try(Connection conn = DriverManager.getConnection(DB_URL);
            Statement stmt = conn.createStatement();
        ) {		      
            /*String sql = "SELECT * FROM challenges";// this is the statement
            ResultSet rs = stmt.executeQuery(sql);// this block of code outputs a select statement
            ArrayList<String> results = new ArrayList<>();
            int id = 0;
            while(rs.next()){
            id = rs.getInt("id");
            results.add(rs.getString("username"));
            results.add(rs.getString("password"));
            results.add(rs.getString("method"));
            results.add(rs.getString("challenge"));
            System.out.println(id + ":" + results);
            results.clear();
            }*/
            //stmt.executeUpdate(sql); //this has the power to update the DB
            Scanner input = new Scanner(System.in);
            File file = null;
            try{
                file = new File(args[0]);
            } catch(ArrayIndexOutOfBoundsException e){
                System.out.println("No argument was provided please provide a file");
                String fileInput = input.nextLine();
                file = new File(fileInput);
            }
            Scanner fileScanner = null; 
            Boolean worked = true;
            try{
                fileScanner = new Scanner(file);
            } catch( FileNotFoundException fnf ){
                worked = false;
                while(!worked){
                    System.out.println("File not found try another file");
                    String fileInput = input.nextLine();
                    file = new File(fileInput);
                    try{
                        fileScanner = new Scanner(file);
                        worked = true;
                    } catch (FileNotFoundException fnf2){
                        worked = false;
                    }
                }
            }
            String output;
            String[] outputArray = new String[4];
            System.out.println("How many lines from the top do you want removed");
            int i = input.nextInt();
            int j = 0;
            if(fileScanner.hasNext() && i>0){
                while (fileScanner.hasNext() && j<i) {
                    fileScanner.nextLine();
                    j++;
                }
            }
            String username = null;
            String password = null;
            String method = null;
            System.out.println("What challenge is this");
            input.nextLine();
            String challenge = input.nextLine();
            byte choice = 0;
            while(fileScanner.hasNext()){
                output = fileScanner.nextLine();
                outputArray = output.split("    ");
                try{
                    username = outputArray[1];
                    password = outputArray[2];
                    method = outputArray[3];
                    String sql = "INSERT INTO challenges (username, password, method, challenge) VALUES(\""+ username + "\", \"" + password + "\", \"" + method + "\", \"" + challenge + "\")";
                    System.out.println("Your sql query is " + sql);
                    System.out.println("Do you want to execute(0) or make a change to username(1), password(2), or method(3)");
                    choice = input.nextByte();
                    input.nextLine();
                    switch(choice){
                        case 0:
                            stmt.executeUpdate(sql);
                            System.out.println("sql ran");
                            break;
                        case 1:
                            System.out.println("What should the new username be");
                            username = input.nextLine();
                            sql = "INSERT INTO challenges (username, password, method, challenge) VALUES(\""+ username + "\", \"" + password + "\", \"" + method + "\", \"" + challenge + "\")";
                            System.out.println("Your sql query is " + sql);
                            System.out.println("Do you want to execute(0) or exit(1)");
                            choice = input.nextByte();
                            if(choice != 0){
                                System.out.println("Please enter manually");
                                System.exit(0);
                            }
                            break;
                        case 2:
                            System.out.println("What should the new password be");
                            password = input.nextLine();
                            sql = "INSERT INTO challenges (username, password, method, challenge) VALUES(\""+ username + "\", \"" + password + "\", \"" + method + "\", \"" + challenge + "\")";
                            System.out.println("Your sql query is " + sql);
                            System.out.println("Do you want to execute(0) or exit(1)");
                            choice = input.nextByte();
                            if(choice != 0){
                                System.out.println("Please enter manually");
                                System.exit(0);
                            }
                            break;
                        case 3:
                            System.out.println("What should the new method be");
                            method = input.nextLine();
                            sql = "INSERT INTO challenges (username, password, method, challenge) VALUES(\""+ username + "\", \"" + password + "\", \"" + method + "\", \"" + challenge + "\")";
                            System.out.println("Your sql query is " + sql);
                            System.out.println("Do you want to execute(0) or exit(1)");
                            choice = input.nextByte();
                            if(choice != 0){
                                System.out.println("Please enter manually");
                                System.exit(0);
                            }
                            break;
                    }
                }catch (ArrayIndexOutOfBoundsException e){
                    System.err.println(output);
                }
            }


        } catch (SQLException e) {
            e.printStackTrace();
        } 
    }
}
