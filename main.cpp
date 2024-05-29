#include <iostream>
#include <thread>
#include <chrono>

int main()
{

    std::this_thread::sleep_for(std::chrono::seconds(5));
    std::cout << "Hello" << std::endl;

    return 0;
}