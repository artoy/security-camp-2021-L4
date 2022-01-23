import java.util.Random;

class Randoms {
  public static void main(String[] arg) {
    Random random = new Random();
    System.out.print(random.nextInt() + " " + random.nextInt() + " ");
    System.out.println(random.nextInt());
  }
}