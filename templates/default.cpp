#include <iostream>
using namespace std;

// Codeforces 999A
int main(){
    ios::sync_with_stdio(false);
    int n, k, x, l=-1, r=-2;
    cin >> n >> k;
    for(int i = 0; i < n; i++) {
        cin >> x;
        if (x > k) {
            if (l < 0) l = i;
            r = i;
        }
    }
    cout << n - (r - l + 1) << endl;
}
