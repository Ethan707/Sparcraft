#ifndef WIN32
#define APIENTRY
#define APIENTRYP
#endif

#include "../SparCraft.h"
#include "SearchExperiment.h"

int main(int argc, char *argv[])
{
    SparCraft::init();

    try
    {
        if (argc == 3)
        {
            SparCraft::SearchExperiment exp(argv[1], argv[2]);
            exp.runExperiment();
        }
        else
        {
            SparCraft::System::FatalError(
                "Please provide experiment file as only argument");
        }
    }
    catch (int e)
    {
        if (e == SparCraft::System::SPARCRAFT_FATAL_ERROR)
        {
            std::cerr << "\nSparCraft FatalError Exception, Shutting Down\n\n";
        }
        else
        {
            std::cerr << "\nUnknown Exception, Shutting Down\n\n";
        }
    }

    return 0;
}
