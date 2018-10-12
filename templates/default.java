import java.util.Scanner;
import java.io.PrintWriter;

public class A {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);
        PrintWriter out = new PrintWriter(System.out);
        int n = in.nextInt();
        int k = in.nextInt();
        int l = -1, r = -2;
        for (int i = 0; i < n; i++) {
            int x = in.nextInt();
            if (x > k) {
                if (l < 0) l = i;
                r = i;
            }
        }
        out.println(n - (r - l + 1));
        in.close();
        out.close();
    }
}